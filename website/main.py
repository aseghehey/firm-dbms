from crypt import methods
import pwd
import re
from tkinter import E
from django.shortcuts import render
from flask import Flask, render_template, redirect, url_for, request, session, flash
import sqlalchemy
from queries import * 
import os 
from dotenv import load_dotenv
import dotenv
from datetime import date
from decimal import *
from mysql.connector import Error
from password_generator import PasswordGenerator

app = Flask(__name__)
app.config['SECRET_KEY']=os.getenv('secret_key')
app.config['SQLALCHEMY_DATABASE_URI']=f"mysql://root:{os.getenv('password')}@localhost/investment_bank"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

@app.route('/')
def home():
    cursor, connection = connectToDB()
    res = displayLocations(cursor,connection)
    data = []
    for vals in res:
        data.append({"location":vals[0]})
    title = 'Beyond Brokerage'
    logged=False
    if 'loggedin' in session:
        logged=True
    return render_template('base.html', title=title,data=data,logged=logged)

@app.route('/about')
def about():
    cursor, connection = connectToDB()
    res = displayTopBrokers(cursor,connection)
    data = []
    for vals in res:
        data.append({'fname': vals[0], 'lname': vals[1], 'totalearnings': vals[2]})
    return render_template('about.html',title="About Us",data=data)

@app.route('/login', methods=['GET','POST'])
def login():
    msg=''
    option=0
    invalid=False
    cursor,connection=connectToDB()
    if request.method=='POST' and 'userid' in request.form and 'password' in request.form:
        mID = request.form.get('userid')
        pw = request.form.get('password')
        if "4444" in str(mID): #Manager
            cursor.execute(f"SELECT * FROM Manager WHERE EID={mID};")
            option=1
        elif "5123" in str(mID): # Broker
            cursor.execute(f"SELECT * FROM Brokers WHERE EID={mID};")
            option=2
        else: # Client
            cursor.execute(f"SELECT * FROM Clients WHERE ClientID={mID};")
            option=3
        acc = cursor.fetchone()
        if acc:
            session['loggedin']=True
            session['id'] = mID
            if option==1:
                if str(acc[1]) == str(pw):
                    session['name'] = 'manager'
                    session['username'] = (str(acc[2]) + ' ' + str(acc[3]))
                    return redirect(url_for('manager'))
                else:
                    flash('Invalid Password or ID')
                    return redirect(url_for('login'))
            elif option==2:
                if str(acc[3] == str(pw)):
                    session['name'] = 'broker'
                    session['username'] = (str(acc[1]) + ' ' + str(acc[2]))
                    return redirect(url_for('broker'))
                else:
                    flash('Invalid Password or ID')
                    return redirect(url_for('login'))
            elif option==3:
                if str(acc[3] == str(pw)):
                    session['name'] = 'client'
                    session['username'] = (str(acc[1]) + ' ' + str(acc[2]))
                    return redirect(url_for('client'))
                else:
                    flash('Invalid Password or ID')
                    return redirect(url_for('login'))
        else:
            flash('Unsucessful. Verify your details.')
            return redirect(url_for('login'))

    return render_template('login.html', title="Login")

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   session.pop('name',None)
   # Redirect to login page
   return redirect(url_for('home'))

@app.route('/manager', methods=['GET','POST'])
def manager():
    cursor,connection = connectToDB()
    name=displayName(cursor,connection,session['id'],'manager')
    branch=displayBranchByManager(cursor,connection,session['id'])
    res = displayBranchByManager(cursor,connection,session['id'])
    res2 = displayBrokers(cursor, connection, res)
    data = []
    for d in res2:
        data.append({'id': d[0],'fname': d[1], 'lname':d[2], 'startdate':d[4], 'salary': d[5]})
    return render_template('manager.html',title="Manager",branch=branch, tp=ProfitByBranch(cursor,connection,branch), data=data)

@app.route('/investment', methods=['GET','POST'])
def investment():
    cursor, connection = connectToDB()
    cursor.execute("SELECT * FROM Investment;")
    data = []
    for vals in cursor.fetchall():
        data.append({"invID":vals[0],"invType":vals[1],"invName":vals[2],"invRA":vals[3],"price":vals[-1]})

    if request.method=='POST':
        if request.form['submitbtn'] == 'remove':
            print('remove toggled')
        elif request.form['submitbtn'] == 'purchase': # for client
            pass

    return render_template('inv.html',title="Investment", data=data)

@app.route('/invchanges',methods=['GET','POST'])
def invchanges():
    cursor,connection=connectToDB()
    #  and {'invID','invType','invName','invRA'} in request.form
    if request.method=='POST' and (session['name'] == 'manager'):
        IID = request.form.get('invID')
        Type = request.form.get('invType')
        Name = request.form.get('invName')
        RA = request.form.get('invRA')
        price2add = request.form.get('invPrice')
        if (int(price2add) > 0) and (100 >= int(RA) >= 0) and str(IID).isdigit():
            cursor.execute(f"select * from investment where type ='{Type}' AND Name='{Name}' OR IID={IID};")
            if not cursor.fetchone():
                addInvestment(cursor,connection, IID,Type,Name,RA,Decimal(price2add))
                return redirect(url_for('investment'))
            else:
                flash('There already exists an investment with the given details')
                return redirect(url_for('invchanges'))
        else:
            flash('Could not add Investment. Make sure it meets the following criteria: Price needs to be positive, Risk Assessment needs to be between 0 and 100 and Invesment ID needs to be an integer')
            return redirect(url_for('invchanges'))
    elif request.method == 'POST' and (session['name'] == 'client'):
        invType = request.form.get('buytype')
        invName = request.form.get('buyname')
        invQty = request.form.get('quantity')
        # if PriceFinder(cursor,connection, invType, invName):
        if (PriceFinder(cursor,connection, invType, invName)) is None:
            flash('Could not find an investment with the given name and type')
            return redirect(url_for('invchanges'))
        else:
            price = PriceFinder(cursor,connection, invType, invName)
            totalprice = (int(price[-1])*int(invQty))
            balance = ClientBalance(cursor, connection, session['id'])
            if canAfford(totalprice, int(balance[-1])):
                updatedbalance = int(balance[-1]) - totalprice
                iid = IIDfinder(cursor, connection, invType,invName)
                today = date.today()
                date2add = today.strftime("%Y-%m-%d")
                # print(iid, session['id'])              
                if not ExistinHasB(cursor,connection,session['id'],iid[0]):
                    addHasBought(cursor,connection,session['id'],iid[0],Decimal(totalprice),invQty,date2add)
                else:
                    curqty = qtyByCIDandIID(cursor, session['id'],iid[0])
                    totalqty = int(curqty)+int(invQty)
                    tp = int(price[-1])*totalqty
                    UpdateQuantity(cursor,connection,session['id'],iid[0],totalqty,Decimal(tp))
                
                updateBalance(cursor,connection,Decimal(updatedbalance),session['id'])
                return redirect(url_for('client'))
            else:
                flash('We apologize but you have insufficient funds to make this purchase')
                return redirect(url_for('invchanges'))
    elif request.method=='POST' and session['name'] == 'broker':
        invPrice = request.form.get('invPrice')
        invRA = request.form.get('invRA')
        invID = request.form.get('invID')
        invalidUpdate = False
        if (100 >= int(invRA) >= 0) and str(invID).isdigit():
            if updatePrice(cursor,connection,invID,Decimal(invPrice), invRA):
                return redirect(url_for('investment'))
            else:
                invalidUpdate=True
        else:
            invalidUpdate = True
        
        if invalidUpdate:
            flash('Could not modify price, make sure ID is correct and RA is between [0,100]')
            return redirect(url_for('invchanges'))

    return render_template('invchanges.html')

@app.route('/removeinv', methods=['GET','POST'])
def removeinv():
    cursor,connection = connectToDB()
    if request.method == 'POST' and session['name'] == 'manager':
        IID = request.form.get('invID')
        if str(IID).isdigit():
            cursor.execute(f'SELECT * FROM Investment WHERE IID={IID};')
            if cursor.fetchone():
                cursor.execute(f'DELETE FROM Investment WHERE IID={IID}')
                connection.commit()
                return redirect(url_for('investment'))
            else:
                flash('Could not find investment')
                return redirect(url_for('removeinv'))
    return render_template('removeinv.html')

@app.route('/broker',methods=['GET','POST'])
def broker():
    cursor, connection = connectToDB()
    res = displayClients(cursor,session['id'])
    data = []
    for v in res:
        data.append({'id': v[0],'name': v[1]+ ' ' + v[2], 'profit': v[5]-v[4], 'balance': v[5], 'add': v[6], 'number': v[7]})
    return render_template('broker.html',title="Broker", data=data)

@app.route('/add', methods=['GET', 'POST'])
def add():
    cursor,connection = connectToDB()
    if request.method=='POST' and session['name'] == 'manager':
        bID = request.form.get('brokerID')
        fn = request.form.get('brokerfn')
        ln = request.form.get('brokerln')
        salary = request.form.get('brokersalary')
        toAddbID = '5123'+ str(bID)
        if str(toAddbID).isdigit() and (int(salary)>0) and (len(bID) == 3):
            cursor.execute(f'select * from brokers where EID = {int(toAddbID)};')
            if cursor.fetchone():
                flash('There already exists a broker with the given ID')
                return redirect(url_for('add'))
            else:
                today = date.today()
                date2add = today.strftime("%Y-%m-%d")
                branch=displayBranchByManager(cursor,connection,session['id'])
                pwo = 'kguvreuw'
                InsertBrokers(cursor,connection, int(toAddbID),fn,ln,str(pwo),date2add,Decimal(salary),branch)
                return redirect(url_for('manager'))
        else:
            flash('Broker ID needs to be an integer, salary cannot be negative and can only give last 3 numbers of Broker ID')
            return redirect(url_for('add'))
    elif request.method=='POST' and session['name'] == 'broker':
        cid = request.form.get('clientID')
        toAddID = '2100' + cid
        fn = request.form.get('clientfn')
        ln = request.form.get('clientln')
        address = request.form.get('address')
        number = request.form.get('number')
        initial = request.form.get('initial')
        invalid = False
        if str(toAddID).isdigit() and (int(initial) > 0) and (len(cid) == 3):
            cursor.execute(f"Select * from Clients where ClientID={int(toAddID)};")
            if not cursor.fetchone():
                pwo = 'jgvkgrb'
                if AddClient(cursor,connection,int(toAddID),fn,ln,pwo,Decimal(initial),Decimal(initial),address,number,session['id']):
                    return redirect(url_for('broker'))
                else:
                    invalid=True
            else:
                invalid = True
        else:
            invalid = True

        if invalid:
            flash('Error adding client. Make sure ClientID is unique, initial amount isn`t negative and is above 10k')
            return redirect(url_for('add'))

    return render_template('add_user.html',title='Add')

@app.route('/sell', methods=['GET','POST'])
def sell():
    cursor,connection = connectToDB()
    if request.method=='POST' and session['name'] == 'client':
        invType = request.form.get('invType')
        invName = request.form.get('invName')
        qty = request.form.get('Quantity')
        invalidSell = False
        msg = ''
        if (PriceFinder(cursor,connection, invType, invName)) is not None:
            curprice = PriceFinder(cursor,connection,invType,invName)[-1]
            invID = IIDfinder(cursor,connection,invType,invName)[0]
            if ExistinHasB(cursor, connection, session['id'],invID):
                curqty = qtyByCIDandIID(cursor,session['id'],invID)
                cursor.execute(f"select CurrentAmount from Clients WHERE ClientID={session['id']}")
                curamnt = cursor.fetchone()[0]
                newamnt = ((int(curprice) * int(qty)) + int(curamnt))
                if (int(curqty) - int(qty) >= 1): # update
                    UpdateCurAmnt(cursor,connection, session['id'],Decimal(newamnt))
                    UpdateQuantityNoPriceChange(cursor,connection, session['id'],invID,(int(curqty) - int(qty)))
                    return redirect(url_for('client'))
                    # if UpdateQuantityNoPriceChange(cursor,connection, session['id'],invID,(int(curqty) - int(qty))) and UpdateCurAmnt(cursor,connection,session['id'],Decimal(newamnt)):
                    #     return redirect(url_for('client'))
                    # else:
                    #     invalidSell=True
                    #     msg='failed1'
                elif (int(curqty) - int(qty) == 0): # delete
                    if DeleteHasBought(cursor,connection,session['id'], invID) and UpdateCurAmnt(cursor,connection,session['id'],Decimal(newamnt)):
                        return redirect(url_for('client'))
                    else:
                        invalidSell=True
                        msg='failed2'
                else: # negative
                    invalidSell = True
                    msg='Invalid quantity. Make sure you input a quantity below or equal to how much you currently own'
            else:
                invalidSell = True
                msg= 'You do not own this investment'
        else:
            invalidSell = True
            msg= 'This investment doesnt exist'

        if invalidSell:
            flash(msg)
            return redirect(url_for('sell'))

    return render_template('sellinv.html', title='Sell')
    
@app.route('/remove', methods=['GET', 'POST'])
def remove():
    cursor,connection = connectToDB()
    if request.method == 'POST' and session['name'] == 'manager':
        bID = request.form.get('brokerID')
        if str(bID).isdigit():
            cursor.execute(f'select * from brokers where EID = {int(bID)};')
            if cursor.fetchone():
                DeleteBroker(cursor,connection, int(bID))
                return redirect(url_for('manager'))
            else:
                flash('Could not find a broker with the given ID')
                return redirect(url_for('remove'))
        else:
            flash('Invalid BrokerID')
            return redirect(url_for('remove'))
    elif request.method == 'POST' and session['name'] == 'broker':
        cID = request.form.get('clientID')
        if str(cID).isdigit():
            if deleteClient(cursor,connection,cID):
                return redirect(url_for('broker'))
            else:
                flash('Could not find ID')
                return redirect(url_for('remove'))

    return render_template('remove_user.html')
    # return render

@app.route('/updatebroker', methods=['GET', 'POST'])
def updatebroker():
    cursor,connection = connectToDB()
    if request.method=='POST':
        bID = request.form.get('brokerID')
        newsal = request.form.get('brokersalary')
        if str(bID).isdigit():
            cursor.execute(f'select * from brokers where EID = {int(bID)};')
            if cursor.fetchone() and (int(newsal) > 0):
                UpdateBrokers(cursor,connection, int(bID), Decimal(newsal))
                return redirect(url_for('manager'))
            else:
                flash('Make sure broker ID exists and new salary is positive!')
                return redirect(url_for('updatebroker'))
        else:
            flash('Make sure Broker ID is integer only')
            return redirect(url_for('updatebroker'))
    return render_template('update_user.html')

@app.route('/client')
def client():
    cursor, connection = connectToDB()
    data = displayInvestmentsByClientID(cursor, connection, session['id'])
    vals = []
    if len(data) >= 1:
        for d in data:
            vals.append({'invName': d[0], 'invType':d[1], 'price':d[2], 'quantity': d[4],'date':d[3]})
    data2 = clientProfile(cursor,connection,session['username'])
    profile = {'profit': (data2[1])-(data2[0]), 'balance': data2[1], 'address': data2[2], 'number': data2[3], 'broker': data2[-1]}
    return render_template('client.html',title="Client",vals=vals,profile=profile)

if __name__ == "__main__":
    app.run(port='8080', debug=True)