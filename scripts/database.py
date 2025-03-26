import os
import psycopg

DB_URL = os.getenv("DATABASE_URL", "postgresql://admin:123@db:5432/shop_db")
def get_connection():
    return psycopg.connect(DB_URL)