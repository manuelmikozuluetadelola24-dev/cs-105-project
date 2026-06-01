"""Database helpers for the Delola Store Product Management System."""

from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import Any, Iterable, Optional, Sequence

import pymysql
import pymysql.cursors


config: list[str] = []


@dataclass(slots=True)
class DatabaseConfig:
    host: str = "localhost"
    database: str = "delola_store"
    user: str = "root"
    password: str = ""

    @classmethod
    def from_config_file(cls, path: str | Path = "config") -> "DatabaseConfig":
        cfg_path = Path(path)

        if not cfg_path.exists():
            return cls()

        raw_lines = [line.rstrip("\n") for line in cfg_path.read_text().splitlines()]
        non_empty = [line.strip() for line in raw_lines if line.strip()]

        # Supports:
        # 2-line config:
        # localhost
        # delola_store
        if len(non_empty) == 2:
            return cls(
                host=non_empty[0],
                database=non_empty[1],
                user="root",
                password="",
            )

        # Supports 4-line config:
        # localhost
        # root
        #
        # delola_store
        if len(raw_lines) >= 4:
            return cls(
                host=raw_lines[0].strip() or "localhost",
                user=raw_lines[1].strip() or "root",
                password=raw_lines[2].strip(),
                database=raw_lines[3].strip() or "delola_store",
            )

        # Supports 3-line config:
        # localhost
        # root
        # delola_store
        if len(non_empty) == 3:
            return cls(
                host=non_empty[0],
                user=non_empty[1],
                password="",
                database=non_empty[2],
            )

        return cls()


def getConfig(path: str | Path = "config") -> list[str]:
    global config
    cfg = DatabaseConfig.from_config_file(path)
    config = [cfg.host, cfg.database, cfg.user, cfg.password]
    return config


def initializeConnection(
    user: Optional[str] = None,
    password: Optional[str] = None,
    *,
    dict_cursor: bool = False,
):
    global config

    if not config:
        getConfig()

    host, database, cfg_user, cfg_password = config[:4]

    cursorclass = pymysql.cursors.DictCursor if dict_cursor else pymysql.cursors.Cursor

    return pymysql.connect(
        host=host,
        user=user or cfg_user or "root",
        password=password if password is not None else cfg_password,
        database=database,
        cursorclass=cursorclass,
        autocommit=False,
    )


def checkUser(db_user: str, db_pass: str) -> bool:
    global config

    if not config:
        getConfig()

    try:
        conn = initializeConnection(db_user, db_pass)
        conn.close()
        config[2] = db_user
        config[3] = db_pass
        return True
    except pymysql.err.MySQLError:
        return False


@contextmanager
def connection(dict_cursor: bool = True):
    conn = initializeConnection(dict_cursor=dict_cursor)

    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


_ALLOWED_DIRECTIONS = {"ASC", "DESC"}

_ALLOWED_COLUMNS = {
    "delivery_id",
    "order_id",
    "delivery_date",
    "status",
    "customer_name",
    "customer_id",
    "product_id",
    "product_name",
    "category_name",
    "stock_quantity",
    "price",
    "order_date",
    "shipment_id",
    "shipment_date",
    "supplier_name",
}


def _order_clause(order_by: str, order: str = "DESC") -> str:
    col = order_by.replace("`", "").split(".")[-1]
    direction = order.upper()

    if col not in _ALLOWED_COLUMNS:
        raise ValueError(f"Unsafe order column: {order_by}")

    if direction not in _ALLOWED_DIRECTIONS:
        raise ValueError(f"Unsafe order direction: {order}")

    return f"`{col}` {direction}"


def _one(sql: str, params: Sequence[Any] = ()) -> Optional[dict[str, Any]]:
    with connection(True) as conn, conn.cursor() as cur:
        cur.execute(sql, params)
        return cur.fetchone()


def _all(sql: str, params: Sequence[Any] = ()) -> list[dict[str, Any]]:
    with connection(True) as conn, conn.cursor() as cur:
        cur.execute(sql, params)
        return list(cur.fetchall())


def _execute(sql: str, params: Sequence[Any] = ()) -> int:
    with connection(True) as conn, conn.cursor() as cur:
        cur.execute(sql, params)
        return cur.lastrowid or cur.rowcount


def outputQueryToConsole(sql: str, result: Iterable[Any]) -> None:
    print(f"Query: {sql}\n")

    for row in result:
        print(row)


def _run_compat(conn, sql: str, params: Sequence[Any] = ()):
    own = conn is None
    conn = conn or initializeConnection(dict_cursor=True)

    try:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()
            outputQueryToConsole(sql, rows)
            return rows
    finally:
        if own:
            conn.close()


def _run_write_compat(conn, sql: str, params: Sequence[Any] = ()):
    own = conn is None
    conn = conn or initializeConnection(dict_cursor=True)

    try:
        with conn.cursor() as cur:
            affected = cur.execute(sql, params)

        conn.commit()
        return affected

    except Exception:
        conn.rollback()
        raise

    finally:
        if own:
            conn.close()


# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------

def get_user_by_credentials(username: str, password: str):
    sql = """
        SELECT *
        FROM users
        WHERE username = %s
        AND password = %s
        LIMIT 1
    """

    return _one(sql, (username, password))


# ---------------------------------------------------------------------------
# Compatibility read/query functions
# ---------------------------------------------------------------------------

def listDeliveries(conn=None, order: str = "DESC", order_by: str = "`DELIVERY`.`delivery_id`"):
    sql = """
        SELECT d.delivery_id, o.order_id, d.delivery_date, d.delivery_street,
               d.delivery_barangay, d.delivery_city, d.delivery_province,
               d.delivered_by, d.status
        FROM DELIVERY d
        JOIN ORDERS o ON d.order_id = o.order_id
    """ + " ORDER BY " + _order_clause(order_by, order)

    return _run_compat(conn, sql)


def filterDeliveriesBy(conn=None, status: str = "'DELIVERED'"):
    status_value = status.strip("'")

    sql = """
        SELECT d.delivery_id, c.customer_name, d.delivery_date, d.status, d.delivered_by
        FROM DELIVERY d
        JOIN ORDERS o ON d.order_id = o.order_id
        JOIN CUSTOMER c ON o.customer_id = c.customer_id
        WHERE d.status = %s
    """

    return _run_compat(conn, sql, (status_value,))


def filterProductByCategory(conn=None, category: str = ""):
    category_value = category.strip("'")

    sql = """
        SELECT p.product_id, p.product_name, p.price, p.stock_quantity
        FROM PRODUCT p
        JOIN PRODUCT_CATEGORY pc ON p.category_id = pc.category_id
        WHERE pc.category_name = %s
    """

    return _run_compat(conn, sql, (category_value,))


def listCustomers(conn=None, order: str = "DESC", order_by: str = "`customer_name`"):
    sql = "SELECT * FROM CUSTOMER ORDER BY " + _order_clause(order_by, order)
    return _run_compat(conn, sql)


def listStockLevel(conn=None, order: str = "ASC", order_by: str = "`stock_quantity`"):
    sql = """
        SELECT p.product_id, p.product_name, pc.category_name, p.stock_quantity, p.price
        FROM PRODUCT p
        JOIN PRODUCT_CATEGORY pc ON p.category_id = pc.category_id
    """ + " ORDER BY " + _order_clause(order_by, order)

    return _run_compat(conn, sql)


def listLowStockLevel(conn=None, low_threshold: str | int = 10):
    sql = """
        SELECT p.product_id, p.product_name, pc.category_name, p.stock_quantity
        FROM PRODUCT p
        JOIN PRODUCT_CATEGORY pc ON p.category_id = pc.category_id
        WHERE p.stock_quantity <= %s
        ORDER BY p.stock_quantity ASC
    """

    return _run_compat(conn, sql, (int(low_threshold),))


def listOrderWithCustomerInfo(conn=None, order: str = "DESC", order_by: str = "`order_date`"):
    sql = """
        SELECT o.order_id, c.customer_name, o.order_date, o.order_type, o.status, o.total_price
        FROM ORDERS o
        JOIN CUSTOMER c ON o.customer_id = c.customer_id
    """ + " ORDER BY " + _order_clause(order_by, order)

    return _run_compat(conn, sql)


def listOrderItemsInOrder(conn=None, with_id: str | int = 0, order: str = "DESC", order_by: str = "`order_id`"):
    sql = """
        SELECT oi.order_item_id, p.product_name, oi.quantity, oi.selling_price,
               (oi.quantity * oi.selling_price) AS item_total
        FROM ORDER_ITEM oi
        JOIN PRODUCT p ON oi.product_id = p.product_id
        WHERE oi.order_id = %s
    """ + " ORDER BY " + _order_clause(order_by, order)

    return _run_compat(conn, sql, (int(with_id),))


def deductFromStock(conn=None, deduct_amount: str = "- 0", with_id: str | int = 0):
    amount = int(deduct_amount.replace("+", "").replace("-", "").strip())

    if deduct_amount.strip().startswith("-"):
        amount = -amount

    sql = "UPDATE PRODUCT SET stock_quantity = stock_quantity + %s WHERE product_id = %s"

    return _run_write_compat(conn, sql, (amount, int(with_id)))


def updateOrderStatus(conn=None, new_status: str = "'PENDING'", with_id: str | int = 0):
    sql = "UPDATE ORDERS SET status = %s WHERE order_id = %s"

    return _run_write_compat(conn, sql, (new_status.strip("'"), int(with_id)))


# ---------------------------------------------------------------------------
# CRUD helpers
# ---------------------------------------------------------------------------

def get_categories():
    return _all("SELECT * FROM PRODUCT_CATEGORY ORDER BY category_name ASC")


def add_category(category_name: str, description: str | None = None) -> int:
    return _execute(
        "INSERT INTO PRODUCT_CATEGORY (category_name, description) VALUES (%s, %s)",
        (category_name, description),
    )


def get_products(order: str = "DESC", order_by: str = "`product_id`"):
    sql = """
        SELECT p.product_id, p.product_name, pc.category_name, p.category_id,
               p.price, p.stock_quantity
        FROM PRODUCT p
        LEFT JOIN PRODUCT_CATEGORY pc ON p.category_id = pc.category_id
    """ + " ORDER BY " + _order_clause(order_by, order)
    
    return _all(sql)

def search_products(term: str):
    return _all("""
        SELECT p.product_id, p.product_name, pc.category_name, p.price, p.stock_quantity
        FROM PRODUCT p
        LEFT JOIN PRODUCT_CATEGORY pc ON p.category_id = pc.category_id
        WHERE p.product_name LIKE %s OR pc.category_name LIKE %s
        ORDER BY p.product_name ASC
    """, (f"%{term}%", f"%{term}%"))


def add_product(product_name: str, category_id: int, price: float | Decimal, stock_quantity: int = 0) -> int:
    return _execute(
        "INSERT INTO PRODUCT (product_name, category_id, price, stock_quantity) VALUES (%s, %s, %s, %s)",
        (product_name, category_id, price, stock_quantity),
    )


def update_product(
    product_id: int,
    product_name: str,
    category_id: int,
    price: float | Decimal,
    stock_quantity: int,
) -> int:
    return _execute("""
        UPDATE PRODUCT
        SET product_name=%s, category_id=%s, price=%s, stock_quantity=%s
        WHERE product_id=%s
    """, (product_name, category_id, price, stock_quantity, product_id))


def delete_product(product_id: int) -> int:
    return _execute("DELETE FROM PRODUCT WHERE product_id=%s", (product_id,))


def get_customers():
    return _all("SELECT * FROM CUSTOMER ORDER BY customer_id DESC")


def search_customers(term: str):
    return _all("""
        SELECT * FROM CUSTOMER
        WHERE customer_name LIKE %s OR contact_number LIKE %s OR customer_city LIKE %s
        ORDER BY customer_name ASC
    """, (f"%{term}%", f"%{term}%", f"%{term}%"))


def add_customer(
    customer_name: str,
    contact_number: str,
    street: str,
    barangay: str,
    city: str,
    province: str,
) -> int:
    return _execute("""
        INSERT INTO CUSTOMER (
            customer_name,
            contact_number,
            customer_street,
            customer_barangay,
            customer_city,
            customer_province
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (customer_name, contact_number, street, barangay, city, province))


def get_suppliers():
    return _all("SELECT * FROM SUPPLIER ORDER BY supplier_id DESC")


def add_supplier(supplier_name: str, contact_number: str, address: str | None = None) -> int:
    return _execute(
        "INSERT INTO SUPPLIER (supplier_name, contact_number, address) VALUES (%s, %s, %s)",
        (supplier_name, contact_number, address),
    )


def get_orders():
    return listOrderWithCustomerInfo(None)


def create_order(customer_id: int, order_date: str, order_type: str, status: str = "PENDING") -> int:
    return _execute("""
        INSERT INTO ORDERS (customer_id, order_date, order_type, status, total_price)
        VALUES (%s, %s, %s, %s, 0)
    """, (customer_id, order_date, order_type, status))


def add_order_item(order_id: int, product_id: int, quantity: int, selling_price: float | Decimal) -> int:
    with connection(True) as conn, conn.cursor() as cur:
        cur.execute("SELECT stock_quantity FROM PRODUCT WHERE product_id=%s FOR UPDATE", (product_id,))
        product = cur.fetchone()

        if not product:
            raise ValueError("Product not found.")

        if product["stock_quantity"] < quantity:
            raise ValueError("Not enough stock for this order item.")

        cur.execute("""
            INSERT INTO ORDER_ITEM (order_id, product_id, quantity, selling_price)
            VALUES (%s, %s, %s, %s)
        """, (order_id, product_id, quantity, selling_price))

        item_id = cur.lastrowid

        cur.execute(
            "UPDATE PRODUCT SET stock_quantity = stock_quantity - %s WHERE product_id=%s",
            (quantity, product_id),
        )

        _recalculate_order_total(cur, order_id)

        return item_id


def _recalculate_order_total(cur, order_id: int) -> None:
    cur.execute("""
        UPDATE ORDERS o
        SET total_price = COALESCE((
            SELECT SUM(quantity * selling_price)
            FROM ORDER_ITEM
            WHERE order_id=%s
        ), 0)
        WHERE o.order_id=%s
    """, (order_id, order_id))


def get_shipments():
    return _all("""
        SELECT s.shipment_id, sp.supplier_name, s.supplier_id, s.shipment_date,
               s.reference_number, s.status
        FROM SHIPMENT s
        LEFT JOIN SUPPLIER sp ON s.supplier_id = sp.supplier_id
        ORDER BY s.shipment_id DESC
    """)


def create_shipment(
    supplier_id: int,
    shipment_date: str,
    reference_number: str,
    status: str = "PENDING",
) -> int:
    return _execute("""
        INSERT INTO SHIPMENT (supplier_id, shipment_date, reference_number, status)
        VALUES (%s, %s, %s, %s)
    """, (supplier_id, shipment_date, reference_number, status))


def add_shipment_item(
    shipment_id: int,
    product_id: int,
    quantity: int,
    unit_cost: float | Decimal,
) -> int:
    return _execute("""
        INSERT INTO SHIPMENT_ITEM (shipment_id, product_id, quantity, unit_cost)
        VALUES (%s, %s, %s, %s)
    """, (shipment_id, product_id, quantity, unit_cost))


def update_shipment_status(shipment_id: int, status: str) -> int:
    with connection(True) as conn, conn.cursor() as cur:
        cur.execute("SELECT status FROM SHIPMENT WHERE shipment_id=%s FOR UPDATE", (shipment_id,))
        old = cur.fetchone()

        if not old:
            raise ValueError("Shipment not found.")

        cur.execute("UPDATE SHIPMENT SET status=%s WHERE shipment_id=%s", (status, shipment_id))

        if old["status"] != "DELIVERED" and status == "DELIVERED":
            cur.execute("""
                UPDATE PRODUCT p
                JOIN SHIPMENT_ITEM si ON p.product_id = si.product_id
                SET p.stock_quantity = p.stock_quantity + si.quantity
                WHERE si.shipment_id = %s
            """, (shipment_id,))

        return cur.rowcount


def addShipmentItemToProductStockLevel(conn=None):
    sql = """
        UPDATE PRODUCT p
        JOIN SHIPMENT_ITEM si ON p.product_id = si.product_id
        JOIN SHIPMENT s ON si.shipment_id = s.shipment_id
        SET p.stock_quantity = p.stock_quantity + si.quantity
        WHERE s.status = 'DELIVERED'
    """

    return _run_write_compat(conn, sql)


def get_deliveries():
    return listDeliveries(None)


def create_delivery(
    order_id: int,
    delivery_date: str,
    street: str,
    barangay: str,
    city: str,
    province: str,
    delivered_by: str,
    status: str = "PENDING",
) -> int:
    return _execute("""
        INSERT INTO DELIVERY (
            order_id,
            delivery_date,
            delivery_street,
            delivery_barangay,
            delivery_city,
            delivery_province,
            delivered_by,
            status
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (order_id, delivery_date, street, barangay, city, province, delivered_by, status))


def update_delivery_status(delivery_id: int, status: str) -> int:
    return _execute(
        "UPDATE DELIVERY SET status=%s WHERE delivery_id=%s",
        (status, delivery_id),
    )


# ---------------------------------------------------------------------------
# Reports / dashboard
# ---------------------------------------------------------------------------

def get_dashboard_counts() -> dict[str, int]:
    row = _one("""
        SELECT
          (SELECT COUNT(*) FROM PRODUCT) AS total_products,
          (SELECT COUNT(*) FROM PRODUCT WHERE stock_quantity <= 10) AS low_stock,
          (SELECT COUNT(*) FROM ORDERS WHERE status = 'PENDING') AS pending_orders,
          (SELECT COUNT(*) FROM DELIVERY WHERE status IN ('PENDING', 'SHIPPED')) AS pending_deliveries
    """)

    return dict(row or {})


def get_inventory_stock_report():
    return listStockLevel(None, "ASC", "`stock_quantity`")


def get_low_stock_alert_report(threshold: int = 10):
    return listLowStockLevel(None, threshold)


def get_sales_report(start_date: str | None = None, end_date: str | None = None):
    params: list[Any] = []
    where = ""

    if start_date and end_date:
        where = "WHERE o.order_date BETWEEN %s AND %s"
        params.extend([start_date, end_date])

    return _all(f"""
        SELECT o.order_id, c.customer_name, o.order_date, o.order_type, o.status, o.total_price
        FROM ORDERS o
        JOIN CUSTOMER c ON o.customer_id = c.customer_id
        {where}
        ORDER BY o.order_date DESC
    """, params)


def get_order_items_detail_report():
    return _all("""
        SELECT o.order_id, c.customer_name, p.product_name, oi.quantity,
               oi.selling_price, (oi.quantity * oi.selling_price) AS item_total
        FROM ORDER_ITEM oi
        JOIN ORDERS o ON oi.order_id = o.order_id
        JOIN CUSTOMER c ON o.customer_id = c.customer_id
        JOIN PRODUCT p ON oi.product_id = p.product_id
        ORDER BY o.order_id DESC
    """)


def get_supplier_shipment_report():
    return _all("""
        SELECT sp.supplier_name, s.shipment_id, s.shipment_date,
               s.reference_number, s.status
        FROM SHIPMENT s
        JOIN SUPPLIER sp ON s.supplier_id = sp.supplier_id
        ORDER BY s.shipment_date DESC
    """)


def get_shipment_items_report():
    return _all("""
        SELECT s.shipment_id, s.reference_number, p.product_name,
               si.quantity, si.unit_cost, (si.quantity * si.unit_cost) AS item_total
        FROM SHIPMENT_ITEM si
        JOIN SHIPMENT s ON si.shipment_id = s.shipment_id
        JOIN PRODUCT p ON si.product_id = p.product_id
        ORDER BY s.shipment_id DESC
    """)


def get_delivery_status_report():
    return (
        filterDeliveriesBy(None, "'PENDING'")
        + filterDeliveriesBy(None, "'SHIPPED'")
        + filterDeliveriesBy(None, "'DELIVERED'")
    )


def get_revenue_report(start_date: str | None = None, end_date: str | None = None):
    params: list[Any] = []
    where = "WHERE o.status <> 'CANCELLED'"

    if start_date and end_date:
        where += " AND o.order_date BETWEEN %s AND %s"
        params.extend([start_date, end_date])

    return _all(f"""
        SELECT DATE(o.order_date) AS order_date,
               COUNT(*) AS order_count,
               SUM(o.total_price) AS revenue
        FROM ORDERS o
        {where}
        GROUP BY DATE(o.order_date)
        ORDER BY DATE(o.order_date) DESC
    """, params)


def get_top_selling_products(limit: int = 10):
    return _all("""
        SELECT p.product_name,
               SUM(oi.quantity) AS units_sold,
               SUM(oi.quantity * oi.selling_price) AS sales_amount
        FROM ORDER_ITEM oi
        JOIN PRODUCT p ON oi.product_id = p.product_id
        GROUP BY p.product_id, p.product_name
        ORDER BY units_sold DESC
        LIMIT %s
    """, (limit,))


def get_customer_order_history(customer_id: int):
    return _all("""
        SELECT o.order_id, o.order_date, o.order_type, o.status, o.total_price
        FROM ORDERS o
        WHERE o.customer_id = %s
        ORDER BY o.order_date DESC
    """, (customer_id,))

def get_suppliers():
    return _all("SELECT * FROM SUPPLIER ORDER BY supplier_id DESC")


def add_supplier(supplier_name: str, contact_number: str, address: str | None = None):
    return _execute("""
        INSERT INTO SUPPLIER (
            supplier_name,
            contact_number,
            supplier_street,
            supplier_barangay,
            supplier_city,
            supplier_province
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        supplier_name,
        contact_number,
        address or "",
        "",
        "",
        "",
    ))