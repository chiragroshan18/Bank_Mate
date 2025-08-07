# db_config.py
import mysql.connector
from mysql.connector import Error
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='bank_system.log'
)

def get_db_connection():
    """Safe database connection with timeout and automatic reconnection"""
    try:
        conn = mysql.connector.connect(
            host='localhost',
            database='pybank',
            user='root',
            password='Enter the pass',
            connect_timeout=5,
            autocommit=True
        )
        if conn.is_connected():
            cursor = conn.cursor(buffered=True)
            return conn, cursor
        raise ConnectionError("Failed to connect to database")
    except Error as e:
        logging.error(f"Database error: {str(e)}")
        raise ConnectionError(f"Database connection failed: {str(e)}")
