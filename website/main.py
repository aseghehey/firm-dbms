from crypt import methods
import pwd
from django.shortcuts import render
from flask import Flask, render_template, redirect, url_for, request, session, flash
import sqlalchemy
from emanconnection import * 
import os 
from dotenv import load_dotenv
import dotenv

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
    return render_template('about.html',title="About Us")

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
    return render_template('manager.html',title="Manager",branch=branch)

@app.route('/brokersmanage')
def managebroker():
    cursor,connection = connectToDB()
    res = displayBranchByManager(cursor,connection,session['id'])
    res2 = displayBrokers(cursor, connection, res)
    data = []
    for d in res2:
        data.append({'fname': d[1], 'lname':d[2], 'startdate':d[4], 'salary': d[5]})
    return render_template('brokerformanager.html', data=data)

@app.route('/investment', methods=['GET','POST'])
def investment():
    cursor, connection = connectToDB()
    cursor.execute("SELECT * FROM Investment;")
    data = []
    for vals in cursor.fetchall():
        data.append({"invID":vals[0],"invType":vals[1],"invName":vals[2],"invRA":vals[-1]})

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
        addInvestment(cursor,connection, IID,Type,Name,RA)
        return redirect(url_for('investment'))
    else:
        pass
    return render_template('invchanges.html')

@app.route('/broker')
def broker():
    return render_template('broker.html',title="Broker")

@app.route('/client')
def client():
    cursor, connection = connectToDB()
    data = displayInvestmentsByClientID(cursor, connection, session['id'])
    vals = []
    if len(data) >= 1:
        for d in data:
            vals.append({'invName': d[0], 'invType':d[1], 'price':d[2],'date':d[3]})
    return render_template('client.html',title="Client",vals=vals)


if __name__ == "__main__":
    app.run(port='8080', debug=True)