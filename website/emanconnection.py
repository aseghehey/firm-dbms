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

def clientProfile(cursor, connection, fullname):
    cursor.execute(f"select InitialAmount, CurrentAmount, Address, TelephoneNumber, BrokerName from customerview WHERE CONCAT(FirstName, ' ', LastName) = '{fullname}';")
    return cursor.fetchone()

def displayTopBrokers(cursor, connection):
    cursor.execute("SELECT FirstName, LastName, TotalEarnings FROM topbrokers;")
    return cursor.fetchall()

def PriceFinder(cursor, connection, Type, Name):
    cursor.execute(f"select Price from Investment where investment.Type= '{Type}' and investment.Name= '{Name}';")
    return cursor.fetchone()

def ClientBalance(cursor, connection, ClientID):
    cursor.execute(f"select currentAmount from Clients where clientID= '{ClientID}';")
    return cursor.fetchone()

def canAfford(askingprice, balance):
    return askingprice < balance

def displayInvestmentsByClientID(cursor, connection, CID):
    cursor.execute(f'SELECT I.Name, I.Type, H.Price, H.DateBought, H.Quantity FROM hasbought H, Investment I WHERE H.InvestmentID = I.IID AND H.ClientID = {CID};')
    return cursor.fetchall()

def addInvestment(cursor,connection, IID,Type,Name,Risk_Assessment,price):
    cursor.execute(f"insert into Investment (IID, Type, Name, Risk_Assessment,Price) values ({IID}, '{Type}', '{Name}', {Risk_Assessment},{price});")
    connection.commit()
    # cursor.close()

def IIDfinder(cursor, connection, Type, Name):
    cursor.execute(f"select IID from Investment where investment.Type= '{Type}' and investment.Name= '{Name}';")
    return cursor.fetchone()

def updateBalance(cursor, connection, newbalance, id):
    cursor.execute(f'update clients set currentAmount ={newbalance}  where clientid ={id}')
    connection.commit()

def addHasBought(cursor,connection, CID, IID, price, qty, date):
    cursor.execute(f"insert into HasBought (ClientID, InvestmentID, Price, DateBought, Quantity) values ({CID}, {IID}, {price}, '{date}', {qty});")
    connection.commit()

def qtyByCIDandIID(cursor,CID,IID):
    cursor.execute(f"Select Quantity from HasBought WHERE ClientID={CID} AND InvestmentID = {IID};")
    return cursor.fetchone()[0]

def ExistinHasB(cursor,connection,CID,IID):
    cursor.execute(f"SELECT * from HasBought WHERE ClientID={CID} AND InvestmentID={IID};")
    if cursor.fetchone() is not None:
        return True
    else:
        return False

def UpdateQuantity(cursor, connection, ClientID, InvestmentID, Quantity,price):
    cursor.execute(f"UPDATE hasbought set quantity={Quantity},price={price} where ClientID = {ClientID} AND InvestmentID ={InvestmentID};")
    connection.commit()

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
    cursor.execute(f"SELECT BranchID FROM Branches WHERE Manager={MID};")
    return cursor.fetchone()[0]

