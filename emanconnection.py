from matplotlib.pyplot import connect
import mysql.connector
from mysql.connector import Error
import os 
from dotenv import load_dotenv
import dotenv

load_dotenv()
connection = mysql.connector.connect(host='localhost',database='investment_bank',user='root',password=os.getenv('password'))
if connection.is_connected():
    cursor = connection.cursor()
    # cursor.execute("SELECT * FROM Clients;")
    # print(cursor.fetchall())

def displayLocations():
    cursor.execute("SELECT Location FROM Branches;")
    return cursor.fetchall()

def AddBrokers(ID, fname, lname, password, startdate, salary, branch):
    try:
        cursor.execute(f"insert into Brokers (EID, first_name, last_name, Password, StartDate, Salary, Branch) values ({ID}, {fname}, {lname}, {password}, {startdate}, {salary}, {branch});")
        connection.commit()
        return "Added broker with success"
    except mysql.connector.Error as err:
        return err

def deleteBrokers(ID):
    try:
        cursor.execute(f"DELETE FROM Brokers WHERE EID={ID};")
        connection.commit()
        return "Removed broker successfully"
    except mysql.connector.Error as err:
        return err

def AddClient(ID, fname, lname, password, iamnt, camnt, address, number, broker):
    try:
        cursor.execute(f"insert into Clients (ClientID, FirstName, LastName, Password, InitialAmount, CurrentAmount, Address, TelephoneNumber, Broker) values ({ID}, {fname}, {lname}, {password},{iamnt}, {camnt}, {address}, {number}, {broker});")
        connection.commit()
        return "Added client with success"
    except mysql.connector.Error as err:
        return err

def deleteClient(ID):
    try:
        cursor.execute(f"DELETE FROM Clients WHERE ClientID={ID};")
        connection.commit()
        return "Removed client successfully"
    except mysql.connector.Error as err:
        return err

def displayInvestments():
    cursor.execute("SELECT Type, Name, Risk_Assessment FROM Investment;")
    return cursor.fetchall()


print(displayInvestments())
