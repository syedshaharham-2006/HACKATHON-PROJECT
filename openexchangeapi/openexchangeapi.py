import pymssql
import json
import requests

def lambda_handler(event, context):

    # ------------------------------
    # FETCH JSON
    # ------------------------------
    APP_ID = "yourappid"
    url = f"https://openexchangerates.org/api/latest.json?app_id={APP_ID}"
    response = requests.get(url)
    data = response.json()

    # ------------------------------
    # CONNECT TO SQL SERVER (RDS)
    # ------------------------------
    conn = pymssql.connect(
        server="",
        user="",
        password="",
        database="",
        port=
    )
    cursor = conn.cursor()

    # ------------------------------
    # CREATE DATABASE IF NOT EXISTS
    # ------------------------------
    cursor.execute("""
        IF DB_ID('forexdb') IS NULL
        CREATE DATABASE forexdb
    """)
    conn.commit()
    conn.close()

    # ------------------------------
    # CONNECT TO forexdb
    # ------------------------------
    conn = pymssql.connect(
        server="database-1.ccleawqo20rf.us-east-1.rds.amazonaws.com",
        user="admin",
        password="Strongpass123!",
        database="forexdb",
        port=1433
    )
    cursor = conn.cursor()

    # ------------------------------
    # CREATE TABLE IF NOT EXISTS
    # ------------------------------
    cursor.execute("""
        IF OBJECT_ID('dbo.ForexData', 'U') IS NULL
        CREATE TABLE ForexData (
            id INT IDENTITY(1,1) PRIMARY KEY,
            symbol NVARCHAR(50),
            price FLOAT,
            timestamp NVARCHAR(50)
        )
    """)
    conn.commit()

    # ------------------------------
    # INSERT JSON DATA
    # ------------------------------
    timestamp = data["timestamp"]
    rates = data["rates"]

    for symbol, price in rates.items():
        cursor.execute("""
            INSERT INTO ForexData (symbol, price, timestamp)
            VALUES (%s, %s, %s)
        """, (symbol, price, str(timestamp)))

    conn.commit()
    conn.close()

    return {
        "statusCode": 200,
        "body": json.dumps("Inserted successfully")
        }