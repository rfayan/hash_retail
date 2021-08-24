from hash_retail.app import create_app, logging_setup
from hash_retail.database import verify_and_create_db_tables

logging_setup()

verify_and_create_db_tables()

app = create_app()
