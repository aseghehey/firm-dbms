from matplotlib.pyplot import connect
import mysql.connector
from mysql.connector import Error
import os 
from dotenv import load_dotenv
import dotenv

load_dotenv()
def connectToDB():
    connection = mysql.connector.connect(host='localhost',database='investment_bank',user='root',password=os.getenv('password'))
    if connection.is_connected():
        cursor = connection.cursor()
    return cursor,connection
    # cursor.execute("SELECT * FROM Clients;")
    # print(cursor.fetchall())

def displayLocations(cursor,connection):
    cursor.execute("SELECT Location FROM Branches;")
    return cursor.fetchall()

def AddBrokers(cursor,connection,ID, fname, lname, password, startdate, salary, branch):
    try:
        cursor.execute(f"insert into Brokers (EID, first_name, last_name, Password, StartDate, Salary, Branch) values ({ID}, {fname}, {lname}, {password}, {startdate}, {salary}, {branch});")
        connection.commit()
        return "Added broker with success"
    except mysql.connector.Error as err:
        return err

def deleteBrokers(cursor, connection,ID):
    try:
        cursor.execute(f"DELETE FROM Brokers WHERE EID={ID};")
        connection.commit()
        return "Removed broker successfully"
    except mysql.connector.Error as err:
        return err

def AddClient(cursor, connection,ID, fname, lname, password, iamnt, camnt, address, number, broker):
    try:
        cursor.execute(f"insert into Clients (ClientID, FirstName, LastName, Password, InitialAmount, CurrentAmount, Address, TelephoneNumber, Broker) values ({ID}, {fname}, {lname}, {password},{iamnt}, {camnt}, {address}, {number}, {broker});")
        connection.commit()
        return "Added client with success"
    except mysql.connector.Error as err:
        return err

def deleteClient(cursor, connection,ID):
    try:
        cursor.execute(f"DELETE FROM Clients WHERE ClientID={ID};")
        connection.commit()
        return "Removed client successfully"
    except mysql.connector.Error as err:
        return err

def displayInvestments(cursor, connection):
    cursor.execute("SELECT Type, Name, Risk_Assessment FROM Investment;")
    return cursor.fetchall()

# test = cursor.execute(f"SELECT * FROM Manager WHERE EID={9876789}")
# print(test)

def findID(cursor, connection,ID,option):
    if option=="client":
        cursor.execute(f"SELECT * FROM Clients WHERE ClientID={ID}")
        return cursor.fetchall()
    elif option=="manager":
        cursor.execute(f"SELECT * FROM Manager WHERE EID={ID}")
        return cursor.fetchall()
    else:
        cursor.execute(f"SELECT * FROM Brokers WHERE EID={ID}")
        return cursor.fetchall()

def displayName(cursor,connection,ID,option):
    if option=='manager':
        cursor.execute(f"SELECT CONCAT(first_name, ' ', last_name) AS NAME FROM Manager WHERE EID={ID}")
        name = cursor.fetchone()
        return name[0]

def displayBrokers(cursor,connection,ID):
    cursor.execute(f"SELECT * FROM Brokers WHERE Branch={ID};")
    res = cursor.fetchall()
    return res

def displayBranchByManager(cursor,connection,MID):
    cursor.execute(f"SELECT * FROM Branches WHERE Manager={MID};")
    return cursor.fetchone()[1]