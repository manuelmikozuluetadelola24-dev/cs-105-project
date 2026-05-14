
## BUILD INSTRUCTIONS
> I removed the .venv folder because it doesn't work on my machine, best not to
> share it in the repository and create your own virtual environment with
> pipenv.  

Run `pipenv --venv` to check if a virtual environment already exists
Run `pipenv install` if not
Run `pipenv lock` then `pipenv sync` to make sure dependencies are properly
installed

# FEATURE IMPLEMENTATION STATUS

### Database
+ Delivery Tracking (/)
+ General Utility Queries (/)
+ Inventory Management (/)
+ Order Processing (/)
+ Reporting (X)
+ Supplier and Shipment (X)

### User Interface

**TODO: Replace python connector function calls with functions from db.py
