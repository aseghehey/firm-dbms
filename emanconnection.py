import mysql.connector
from mysql.connector import Error
import os 
from dotenv import load_dotenv
import dotenv

load_dotenv()
try:
    connection = mysql.connector.connect(host='localhost',database='investment_bank',user='root',password=os.getenv('password'))
    if connection.is_connected():
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Clients;")
        print(cursor.fetchall())
except Error as err:
    print("error: ", err)