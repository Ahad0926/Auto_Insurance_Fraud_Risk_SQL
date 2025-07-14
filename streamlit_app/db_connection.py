import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Admin123",
        database="auto_insurance_db"
    )
