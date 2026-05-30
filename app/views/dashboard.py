"""
db.py - Database module for Delola Store Product Management System
Provides full CRUD, reporting, and utility operations for all tables.
"""

import logging
import mysql.connector
from mysql.connector import Error
from dataclasses import dataclass, field
from typing import Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

@dataclass
class DatabaseConfig:
    host: str = "localhost"
    user: str = "root"
    password: str = ""
    database: str = "delola_store"
    port: int = 3306


# ---------------------------------------------------------------------------
# Core Database class
# ---------------------------------------------------------------------------

class Database:
    """All database operations for the Delola Store system."""

    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.connection = None
        self.cursor = None
        self.connect()

    # ------------------------------------------------------------------
    # Connection management
    # ------------------------------------------------------------------

    def connect(self) -> bool:
        try:
            self.connection = mysql.connector.connect(
                host=self.config.host,
                user=self.config.user,
                password=self.config.password,
                database=self.config.database,
                port=self.config.port,
                autocommit=False,
            )
            self.cursor = self.connection.cursor(dictionary=True)
            logger.info("Connected to database '%s'.", self.config.database)
            return True
        except Error as e:
            logger.error("Connection failed: %s", e)
            return False

    def disconnect(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection and self.connection.is_connected():
                self.connection.close()
                logger.info("Database connection closed.")
        except Error as e:
            logger.error("Error closing connection: %s", e)

    def _execute(self, sql: str, params: tuple = (), fetch: str = "none"):
        """
        Internal helper.  fetch = 'one' | 'all' | 'none'
        Returns rows for fetch queries, lastrowid for INSERT, rowcount for others.
        """
        try:
            self.cursor.execute(sql, params)
            if fetch == "one":
                return self.cursor.fetchone()
            if fetch == "all":
                return self.cursor.fetchall()
            self.connection.commit()
            return self.cursor.lastrowid if self.cursor.lastrowid else self.cursor.rowcount
        except Error as e:
            self.connection.rollback()
            logger.error("Query failed: %s\nSQL: %s\nParams: %s", e, sql, params)
            raise

    # ==================================================================
    # PRODUCT CATEGORY
    # ==================================================================

    def get_all_categories(self) -> list[dict]:
        return self._execute("SELECT * FROM PRODUCT_CATEGORY ORDER BY category_name", fetch="all")

    def get_category(self, category_id: int) -> Optional[dict]:
        return self._execute(
            "SELECT * FROM PRODUCT_CATEGORY WHERE category_id = %s", (category_id,), fetch="one"
        )

    def add_category(self, category_name: str) -> int:
        return self._execute(
            "INSERT INTO PRODUCT_CATEGORY (category_name) VALUES (%s)", (category_name,)
        )

    def update_category(self, category_id: int, category_name: str) -> int:
        return self._execute(
            "UPDATE PRODUCT_CATEGORY SET category_name = %s WHERE category_id = %s",
            (category_name, category_id),
        )

    def delete_category(self, category_id: int) -> int:
        return self._execute(
            "DELETE FROM PRODUCT_CATEGORY WHERE category_id = %s", (category_id,)
        )

    # ==================================================================
    # PRODUCT
    # ==================================================================

    def get_all_products(self) -> list[dict]:
        sql = """
            SELECT p.*, c.category_name
            FROM PRODUCT p
            LEFT JOIN PRODUCT_CATEGORY c ON p.category_id = c.category_id
            ORDER BY p.product_name
        """
        return self._execute(sql, fetch="all")

    def get_product(self, product_id: int) -> Optional[dict]:
        sql = """
            SELECT p.*, c.category_name
            FROM PRODUCT p
            LEFT JOIN PRODUCT_CATEGORY c ON p.category_id = c.category_id
            WHERE p.product_id = %s
        """
        return self._execute(sql, (product_id,), fetch="one")

    def add_product(self, product_name: str, price: float,
                    stock_quantity: int = 0, category_id: Optional[int] = None) -> int:
        return self._execute(
            "INSERT INTO PRODUCT (product_name, price, stock_quantity, category_id) VALUES (%s, %s, %s, %s)",
            (product_name, price, stock_quantity, category_id),
        )

    def update_product(self, product_id: int, product_name: str, price: float,
                       stock_quantity: int, category_id: Optional[int] = None) -> int:
        return self._execute(
            """UPDATE PRODUCT
               SET product_name = %s, price = %s, stock_quantity = %s, category_id = %s
               WHERE product_id = %s""",
            (product_name, price, stock_quantity, category_id, product_id),
        )

    def delete_product(self, product_id: int) -> int:
        return self._execute("DELETE FROM PRODUCT WHERE product_id = %s", (product_id,))

    def update_stock(self, product_id: int, quantity_delta: int) -> int:
        """Add (positive) or subtract (negative) from stock."""
        return self._execute(
            "UPDATE PRODUCT SET stock_quantity = stock_quantity + %s WHERE product_id = %s",
            (quantity_delta, product_id),
        )

    def search_products(self, keyword: str) -> list[dict]:
        sql = """
            SELECT p.*, c.category_name
            FROM PRODUCT p
            LEFT JOIN PRODUCT_CATEGORY c ON p.category_id = c.category_id
            WHERE p.product_name LIKE %s
            ORDER BY p.product_name
        """
        return self._execute(sql, (f"%{keyword}%",), fetch="all")

    # ==================================================================
    # SUPPLIER
    # ==================================================================

    def get_all_suppliers(self) -> list[dict]:
        return self._execute("SELECT * FROM SUPPLIER ORDER BY supplier_name", fetch="all")

    def get_supplier(self, supplier_id: int) -> Optional[dict]:
        return self._execute(
            "SELECT * FROM SUPPLIER WHERE supplier_id = %s", (supplier_id,), fetch="one"
        )

    def add_supplier(self, supplier_name: str, contact_number: str,
                     supplier_street: str, supplier_barangay: str,
                     supplier_city: str, supplier_province: str) -> int:
        return self._execute(
            """INSERT INTO SUPPLIER
               (supplier_name, contact_number, supplier_street,
                supplier_barangay, supplier_city, supplier_province)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (supplier_name, contact_number, supplier_street,
             supplier_barangay, supplier_city, supplier_province),
        )

    def update_supplier(self, supplier_id: int, supplier_name: str, contact_number: str,
                        supplier_street: str, supplier_barangay: str,
                        supplier_city: str, supplier_province: str) -> int:
        return self._execute(
            """UPDATE SUPPLIER SET supplier_name=%s, contact_number=%s, supplier_street=%s,
               supplier_barangay=%s, supplier_city=%s, supplier_province=%s
               WHERE supplier_id=%s""",
            (supplier_name, contact_number, supplier_street,
             supplier_barangay, supplier_city, supplier_province, supplier_id),
        )

    def delete_supplier(self, supplier_id: int) -> int:
        return self._execute("DELETE FROM SUPPLIER WHERE supplier_id = %s", (supplier_id,))

    # ==================================================================
    # SHIPMENT
    # ==================================================================

    def get_all_shipments(self) -> list[dict]:
        sql = """
            SELECT s.*, sup.supplier_name
            FROM SHIPMENT s
            LEFT JOIN SUPPLIER sup ON s.supplier_id = sup.supplier_id
            ORDER BY s.shipment_date DESC
        """
        return self._execute(sql, fetch="all")

    def get_shipment(self, shipment_id: int) -> Optional[dict]:
        sql = """
            SELECT s.*, sup.supplier_name
            FROM SHIPMENT s
            LEFT JOIN SUPPLIER sup ON s.supplier_id = sup.supplier_id
            WHERE s.shipment_id = %s
        """
        return self._execute(sql, (shipment_id,), fetch="one")

    def add_shipment(self, supplier_id: int, shipment_date: str, reference_number: str,
                     status: str = "PENDING") -> int:
        return self._execute(
            "INSERT INTO SHIPMENT (supplier_id, shipment_date, status, reference_number) VALUES (%s, %s, %s, %s)",
            (supplier_id, shipment_date, status, reference_number),
        )

    def update_shipment(self, shipment_id: int, supplier_id: int, shipment_date: str,
                        reference_number: str, status: str) -> int:
        return self._execute(
            """UPDATE SHIPMENT SET supplier_id=%s, shipment_date=%s,
               reference_number=%s, status=%s WHERE shipment_id=%s""",
            (supplier_id, shipment_date, reference_number, status, shipment_id),
        )

    def update_shipment_status(self, shipment_id: int, status: str) -> int:
        """Update status; if DELIVERED, automatically add stock from shipment items."""
        if status == "DELIVERED":
            items = self.get_shipment_items(shipment_id)
            for item in items:
                self.update_stock(item["product_id"], item["quantity"])
        return self._execute(
            "UPDATE SHIPMENT SET status=%s WHERE shipment_id=%s", (status, shipment_id)
        )

    def delete_shipment(self, shipment_id: int) -> int:
        return self._execute("DELETE FROM SHIPMENT WHERE shipment_id = %s", (shipment_id,))

    # ==================================================================
    # SHIPMENT ITEM
    # ==================================================================

    def get_shipment_items(self, shipment_id: int) -> list[dict]:
        sql = """
            SELECT si.*, p.product_name
            FROM SHIPMENT_ITEM si
            JOIN PRODUCT p ON si.product_id = p.product_id
            WHERE si.shipment_id = %s
        """
        return self._execute(sql, (shipment_id,), fetch="all")

    def add_shipment_item(self, shipment_id: int, product_id: int,
                          quantity: int, unit_cost: float) -> int:
        return self._execute(
            "INSERT INTO SHIPMENT_ITEM (shipment_id, product_id, quantity, unit_cost) VALUES (%s, %s, %s, %s)",
            (shipment_id, product_id, quantity, unit_cost),
        )

    def update_shipment_item(self, shipment_item_id: int, quantity: int, unit_cost: float) -> int:
        return self._execute(
            "UPDATE SHIPMENT_ITEM SET quantity=%s, unit_cost=%s WHERE shipment_item_id=%s",
            (quantity, unit_cost, shipment_item_id),
        )

    def delete_shipment_item(self, shipment_item_id: int) -> int:
        return self._execute(
            "DELETE FROM SHIPMENT_ITEM WHERE shipment_item_id = %s", (shipment_item_id,)
        )

    # ==================================================================
    # CUSTOMER
    # ==================================================================

    def get_all_customers(self) -> list[dict]:
        return self._execute("SELECT * FROM CUSTOMER ORDER BY customer_name", fetch="all")

    def get_customer(self, customer_id: int) -> Optional[dict]:
        return self._execute(
            "SELECT * FROM CUSTOMER WHERE customer_id = %s", (customer_id,), fetch="one"
        )

    def add_customer(self, customer_name: str, contact_number: str,
                     customer_street: str, customer_barangay: str,
                     customer_city: str, customer_province: str) -> int:
        return self._execute(
            """INSERT INTO CUSTOMER
               (customer_name, contact_number, customer_street,
                customer_barangay, customer_city, customer_province)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (customer_name, contact_number, customer_street,
             customer_barangay, customer_city, customer_province),
        )

    def update_customer(self, customer_id: int, customer_name: str, contact_number: str,
                        customer_street: str, customer_barangay: str,
                        customer_city: str, customer_province: str) -> int:
        return self._execute(
            """UPDATE CUSTOMER SET customer_name=%s, contact_number=%s, customer_street=%s,
               customer_barangay=%s, customer_city=%s, customer_province=%s
               WHERE customer_id=%s""",
            (customer_name, contact_number, customer_street,
             customer_barangay, customer_city, customer_province, customer_id),
        )

    def delete_customer(self, customer_id: int) -> int:
        return self._execute("DELETE FROM CUSTOMER WHERE customer_id = %s", (customer_id,))

    def search_customers(self, keyword: str) -> list[dict]:
        return self._execute(
            "SELECT * FROM CUSTOMER WHERE customer_name LIKE %s ORDER BY customer_name",
            (f"%{keyword}%",), fetch="all",
        )

    # ==================================================================
    # ORDERS
    # ==================================================================

    def get_all_orders(self) -> list[dict]:
        sql = """
            SELECT o.*, c.customer_name
            FROM ORDERS o
            LEFT JOIN CUSTOMER c ON o.customer_id = c.customer_id
            ORDER BY o.order_date DESC
        """
        return self._execute(sql, fetch="all")

    def get_order(self, order_id: int) -> Optional[dict]:
        sql = """
            SELECT o.*, c.customer_name
            FROM ORDERS o
            LEFT JOIN CUSTOMER c ON o.customer_id = c.customer_id
            WHERE o.order_id = %s
        """
        return self._execute(sql, (order_id,), fetch="one")

    def create_order(self, customer_id: int, order_date: str, order_type: str,
                     status: str = "PENDING", total_price: float = 0.0) -> int:
        return self._execute(
            """INSERT INTO ORDERS (customer_id, order_date, status, total_price, order_type)
               VALUES (%s, %s, %s, %s, %s)""",
            (customer_id, order_date, status, total_price, order_type),
        )

    def update_order(self, order_id: int, customer_id: int, order_date: str,
                     order_type: str, status: str) -> int:
        return self._execute(
            """UPDATE ORDERS SET customer_id=%s, order_date=%s, order_type=%s, status=%s
               WHERE order_id=%s""",
            (customer_id, order_date, order_type, status, order_id),
        )

    def update_order_status(self, order_id: int, status: str) -> int:
        return self._execute(
            "UPDATE ORDERS SET status=%s WHERE order_id=%s", (status, order_id)
        )

    def delete_order(self, order_id: int) -> int:
        return self._execute("DELETE FROM ORDERS WHERE order_id = %s", (order_id,))

    def _recalculate_order_total(self, order_id: int):
        """Recalculate and update order total_price from its items."""
        result = self._execute(
            "SELECT SUM(quantity * selling_price) AS total FROM ORDER_ITEM WHERE order_id = %s",
            (order_id,), fetch="one",
        )
        total = result["total"] or 0.0
        self._execute(
            "UPDATE ORDERS SET total_price=%s WHERE order_id=%s", (total, order_id)
        )

    # ==================================================================
    # ORDER ITEM
    # ==================================================================

    def get_order_items(self, order_id: int) -> list[dict]:
        sql = """
            SELECT oi.*, p.product_name
            FROM ORDER_ITEM oi
            JOIN PRODUCT p ON oi.product_id = p.product_id
            WHERE oi.order_id = %s
        """
        return self._execute(sql, (order_id,), fetch="all")

    def add_order_item(self, order_id: int, product_id: int,
                       quantity: int, selling_price: float) -> int:
        """Add item, deduct stock, and recalculate order total."""
        item_id = self._execute(
            "INSERT INTO ORDER_ITEM (order_id, product_id, quantity, selling_price) VALUES (%s, %s, %s, %s)",
            (order_id, product_id, quantity, selling_price),
        )
        self.update_stock(product_id, -quantity)
        self._recalculate_order_total(order_id)
        return item_id

    def update_order_item(self, order_item_id: int, quantity: int, selling_price: float) -> int:
        """Update quantity, adjusting stock delta, and recalculate order total."""
        old = self._execute(
            "SELECT * FROM ORDER_ITEM WHERE order_item_id=%s", (order_item_id,), fetch="one"
        )
        if old:
            delta = old["quantity"] - quantity  # positive = return to stock
            self.update_stock(old["product_id"], delta)
        result = self._execute(
            "UPDATE ORDER_ITEM SET quantity=%s, selling_price=%s WHERE order_item_id=%s",
            (quantity, selling_price, order_item_id),
        )
        if old:
            self._recalculate_order_total(old["order_id"])
        return result

    def delete_order_item(self, order_item_id: int) -> int:
        """Delete item, restore stock, and recalculate order total."""
        old = self._execute(
            "SELECT * FROM ORDER_ITEM WHERE order_item_id=%s", (order_item_id,), fetch="one"
        )
        result = self._execute(
            "DELETE FROM ORDER_ITEM WHERE order_item_id=%s", (order_item_id,)
        )
        if old:
            self.update_stock(old["product_id"], old["quantity"])
            self._recalculate_order_total(old["order_id"])
        return result

    # ==================================================================
    # IN-STORE ORDER
    # ==================================================================

    def add_in_store_order_details(self, order_id: int,
                                   release_time: Optional[str] = None,
                                   claimed_by: Optional[str] = None) -> int:
        return self._execute(
            "INSERT INTO IN_STORE_ORDER (order_id, release_time, claimed_by) VALUES (%s, %s, %s)",
            (order_id, release_time, claimed_by),
        )

    def get_in_store_order(self, order_id: int) -> Optional[dict]:
        return self._execute(
            "SELECT * FROM IN_STORE_ORDER WHERE order_id=%s", (order_id,), fetch="one"
        )

    def update_in_store_order(self, order_id: int, release_time: Optional[str],
                              claimed_by: Optional[str]) -> int:
        return self._execute(
            "UPDATE IN_STORE_ORDER SET release_time=%s, claimed_by=%s WHERE order_id=%s",
            (release_time, claimed_by, order_id),
        )

    def delete_in_store_order(self, order_id: int) -> int:
        return self._execute(
            "DELETE FROM IN_STORE_ORDER WHERE order_id=%s", (order_id,)
        )

    # ==================================================================
    # DELIVERY ORDER
    # ==================================================================

    def add_delivery_order_details(self, order_id: int,
                                   order_note: Optional[str] = None) -> int:
        return self._execute(
            "INSERT INTO DELIVERY_ORDER (order_id, delivery_note) VALUES (%s, %s)",
            (order_id, order_note),
        )

    def get_delivery_order(self, order_id: int) -> Optional[dict]:
        return self._execute(
            "SELECT * FROM DELIVERY_ORDER WHERE order_id=%s", (order_id,), fetch="one"
        )

    def update_delivery_order(self, order_id: int, order_note: Optional[str]) -> int:
        return self._execute(
            "UPDATE DELIVERY_ORDER SET delivery_note=%s WHERE order_id=%s",
            (order_note, order_id),
        )

    def delete_delivery_order(self, order_id: int) -> int:
        return self._execute("DELETE FROM DELIVERY_ORDER WHERE order_id=%s", (order_id,))

    # ==================================================================
    # DELIVERY
    # ==================================================================

    def get_all_deliveries(self) -> list[dict]:
        sql = """
            SELECT d.*, o.order_date, c.customer_name
            FROM DELIVERY d
            JOIN ORDERS o ON d.order_id = o.order_id
            LEFT JOIN CUSTOMER c ON o.customer_id = c.customer_id
            ORDER BY d.delivery_date DESC
        """
        return self._execute(sql, fetch="all")

    def get_delivery(self, delivery_id: int) -> Optional[dict]:
        return self._execute(
            "SELECT * FROM DELIVERY WHERE delivery_id=%s", (delivery_id,), fetch="one"
        )

    def get_delivery_by_order(self, order_id: int) -> Optional[dict]:
        return self._execute(
            "SELECT * FROM DELIVERY WHERE order_id=%s", (order_id,), fetch="one"
        )

    def create_delivery(self, order_id: int, delivery_date: str,
                        delivery_street: str, delivery_barangay: str,
                        delivery_city: str, delivery_province: str,
                        delivered_by: Optional[str] = None,
                        status: str = "PENDING") -> int:
        return self._execute(
            """INSERT INTO DELIVERY
               (order_id, delivery_date, delivery_street, delivery_barangay,
                delivery_city, delivery_province, delivered_by, status)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (order_id, delivery_date, delivery_street, delivery_barangay,
             delivery_city, delivery_province, delivered_by, status),
        )

    def update_delivery(self, delivery_id: int, delivery_date: str,
                        delivery_street: str, delivery_barangay: str,
                        delivery_city: str, delivery_province: str,
                        delivered_by: Optional[str], status: str) -> int:
        return self._execute(
            """UPDATE DELIVERY SET delivery_date=%s, delivery_street=%s, delivery_barangay=%s,
               delivery_city=%s, delivery_province=%s, delivered_by=%s, status=%s
               WHERE delivery_id=%s""",
            (delivery_date, delivery_street, delivery_barangay,
             delivery_city, delivery_province, delivered_by, status, delivery_id),
        )

    def update_delivery_status(self, delivery_id: int, status: str) -> int:
        return self._execute(
            "UPDATE DELIVERY SET status=%s WHERE delivery_id=%s", (status, delivery_id)
        )

    def delete_delivery(self, delivery_id: int) -> int:
        return self._execute("DELETE FROM DELIVERY WHERE delivery_id=%s", (delivery_id,))

    # ==================================================================
    # REPORTS
    # ==================================================================

    def get_inventory_stock_report(self) -> list[dict]:
        """Full inventory with category and stock."""
        sql = """
            SELECT p.product_id, p.product_name, c.category_name,
                   p.price, p.stock_quantity
            FROM PRODUCT p
            LEFT JOIN PRODUCT_CATEGORY c ON p.category_id = c.category_id
            ORDER BY c.category_name, p.product_name
        """
        return self._execute(sql, fetch="all")

    def get_low_stock_alert_report(self, threshold: int = 10) -> list[dict]:
        """Products with stock at or below threshold."""
        sql = """
            SELECT p.product_id, p.product_name, c.category_name,
                   p.stock_quantity, p.price
            FROM PRODUCT p
            LEFT JOIN PRODUCT_CATEGORY c ON p.category_id = c.category_id
            WHERE p.stock_quantity <= %s
            ORDER BY p.stock_quantity ASC
        """
        return self._execute(sql, (threshold,), fetch="all")

    def get_supplier_shipment_report(self) -> list[dict]:
        """All shipments grouped with supplier info."""
        sql = """
            SELECT s.shipment_id, s.reference_number, s.shipment_date, s.status,
                   sup.supplier_name, sup.contact_number,
                   COUNT(si.shipment_item_id) AS item_count,
                   SUM(si.quantity * si.unit_cost) AS total_cost
            FROM SHIPMENT s
            LEFT JOIN SUPPLIER sup ON s.supplier_id = sup.supplier_id
            LEFT JOIN SHIPMENT_ITEM si ON s.shipment_id = si.shipment_id
            GROUP BY s.shipment_id, s.reference_number, s.shipment_date, s.status,
                     sup.supplier_name, sup.contact_number
            ORDER BY s.shipment_date DESC
        """
        return self._execute(sql, fetch="all")

    def get_sales_report(self, start_date: Optional[str] = None,
                         end_date: Optional[str] = None) -> list[dict]:
        """Orders summary with optional date range."""
        sql = """
            SELECT o.order_id, o.order_date, o.order_type, o.status,
                   c.customer_name, o.total_price
            FROM ORDERS o
            LEFT JOIN CUSTOMER c ON o.customer_id = c.customer_id
            WHERE 1=1
        """
        params: list = []
        if start_date:
            sql += " AND o.order_date >= %s"
            params.append(start_date)
        if end_date:
            sql += " AND o.order_date <= %s"
            params.append(end_date)
        sql += " ORDER BY o.order_date DESC"
        return self._execute(sql, tuple(params), fetch="all")

    def get_order_items_detail_report(self, order_id: Optional[int] = None) -> list[dict]:
        """Detailed order items, optionally filtered by order."""
        sql = """
            SELECT oi.order_item_id, oi.order_id, o.order_date,
                   c.customer_name, p.product_name,
                   oi.quantity, oi.selling_price,
                   (oi.quantity * oi.selling_price) AS subtotal
            FROM ORDER_ITEM oi
            JOIN ORDERS o ON oi.order_id = o.order_id
            LEFT JOIN CUSTOMER c ON o.customer_id = c.customer_id
            JOIN PRODUCT p ON oi.product_id = p.product_id
        """
        params: list = []
        if order_id is not None:
            sql += " WHERE oi.order_id = %s"
            params.append(order_id)
        sql += " ORDER BY o.order_date DESC, oi.order_id"
        return self._execute(sql, tuple(params), fetch="all")

    def get_delivery_status_report(self) -> list[dict]:
        """Delivery records with order and customer info."""
        sql = """
            SELECT d.delivery_id, d.delivery_date, d.status, d.delivered_by,
                   CONCAT(d.delivery_street, ', ', d.delivery_barangay, ', ',
                          d.delivery_city, ', ', d.delivery_province) AS delivery_address,
                   c.customer_name, o.order_id, o.total_price
            FROM DELIVERY d
            JOIN ORDERS o ON d.order_id = o.order_id
            LEFT JOIN CUSTOMER c ON o.customer_id = c.customer_id
            ORDER BY d.delivery_date DESC
        """
        return self._execute(sql, fetch="all")

    def get_shipment_items_report(self, shipment_id: Optional[int] = None) -> list[dict]:
        """Shipment items detail report."""
        sql = """
            SELECT si.shipment_item_id, si.shipment_id, s.reference_number,
                   s.shipment_date, s.status, sup.supplier_name,
                   p.product_name, si.quantity, si.unit_cost,
                   (si.quantity * si.unit_cost) AS line_total
            FROM SHIPMENT_ITEM si
            JOIN SHIPMENT s ON si.shipment_id = s.shipment_id
            LEFT JOIN SUPPLIER sup ON s.supplier_id = sup.supplier_id
            JOIN PRODUCT p ON si.product_id = p.product_id
        """
        params: list = []
        if shipment_id is not None:
            sql += " WHERE si.shipment_id = %s"
            params.append(shipment_id)
        sql += " ORDER BY s.shipment_date DESC"
        return self._execute(sql, tuple(params), fetch="all")

    def get_revenue_report(self, start_date: Optional[str] = None,
                           end_date: Optional[str] = None) -> list[dict]:
        """Daily revenue summary."""
        sql = """
            SELECT o.order_date,
                   COUNT(o.order_id) AS total_orders,
                   SUM(o.total_price) AS total_revenue
            FROM ORDERS o
            WHERE o.status NOT IN ('CANCELLED')
        """
        params: list = []
        if start_date:
            sql += " AND o.order_date >= %s"
            params.append(start_date)
        if end_date:
            sql += " AND o.order_date <= %s"
            params.append(end_date)
        sql += " GROUP BY o.order_date ORDER BY o.order_date DESC"
        return self._execute(sql, tuple(params), fetch="all")

    def get_top_selling_products(self, limit: int = 10) -> list[dict]:
        """Top products by total quantity sold."""
        sql = """
            SELECT p.product_id, p.product_name, c.category_name,
                   SUM(oi.quantity) AS total_sold,
                   SUM(oi.quantity * oi.selling_price) AS total_revenue
            FROM ORDER_ITEM oi
            JOIN PRODUCT p ON oi.product_id = p.product_id
            LEFT JOIN PRODUCT_CATEGORY c ON p.category_id = c.category_id
            JOIN ORDERS o ON oi.order_id = o.order_id
            WHERE o.status NOT IN ('CANCELLED')
            GROUP BY p.product_id, p.product_name, c.category_name
            ORDER BY total_sold DESC
            LIMIT %s
        """
        return self._execute(sql, (limit,), fetch="all")

    def get_customer_order_history(self, customer_id: int) -> list[dict]:
        """All orders for a specific customer."""
        sql = """
            SELECT o.order_id, o.order_date, o.order_type, o.status, o.total_price,
                   COUNT(oi.order_item_id) AS item_count
            FROM ORDERS o
            LEFT JOIN ORDER_ITEM oi ON o.order_id = oi.order_id
            WHERE o.customer_id = %s
            GROUP BY o.order_id, o.order_date, o.order_type, o.status, o.total_price
            ORDER BY o.order_date DESC
        """
        return self._execute(sql, (customer_id,), fetch="all")

    # ==================================================================
    # UTILITY
    # ==================================================================

    def sort_table(self, table: str, column: str, ascending: bool = True) -> list[dict]:
        """
        Generic sort for any table. Only allow known tables/columns to avoid SQL injection.
        """
        allowed_tables = {
            "PRODUCT", "PRODUCT_CATEGORY", "CUSTOMER", "SUPPLIER",
            "ORDERS", "ORDER_ITEM", "SHIPMENT", "SHIPMENT_ITEM", "DELIVERY",
        }
        if table.upper() not in allowed_tables:
            raise ValueError(f"Unknown table: {table}")
        direction = "ASC" if ascending else "DESC"
        # column name validation: alphanumeric + underscore only
        if not column.replace("_", "").isalnum():
            raise ValueError(f"Invalid column name: {column}")
        sql = f"SELECT * FROM {table.upper()} ORDER BY {column} {direction}"
        return self._execute(sql, fetch="all")

    def filter_table(self, table: str, column: str, value) -> list[dict]:
        """Filter any allowed table by an exact column value."""
        allowed_tables = {
            "PRODUCT", "PRODUCT_CATEGORY", "CUSTOMER", "SUPPLIER",
            "ORDERS", "ORDER_ITEM", "SHIPMENT", "SHIPMENT_ITEM", "DELIVERY",
        }
        if table.upper() not in allowed_tables:
            raise ValueError(f"Unknown table: {table}")
        if not column.replace("_", "").isalnum():
            raise ValueError(f"Invalid column name: {column}")
        sql = f"SELECT * FROM {table.upper()} WHERE {column} = %s"
        return self._execute(sql, (value,), fetch="all")


# ---------------------------------------------------------------------------
# Context Manager
# ---------------------------------------------------------------------------

class DatabaseContextManager:
    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.db: Optional[Database] = None

    def __enter__(self) -> Database:
        self.db = Database(self.config)
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.db:
            self.db.disconnect()
        return False  # do not suppress exceptions


# ---------------------------------------------------------------------------
# Default config (edit to match your environment)
# ---------------------------------------------------------------------------

DEFAULT_CONFIG = DatabaseConfig(
    host="localhost",
    user="root",
    password="",
    database="delola_store",
)