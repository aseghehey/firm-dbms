from crypt import methods
import pwd
from django.shortcuts import render
from flask import Flask, render_template, redirect, url_for, request, session
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
    title = 'Investment Bank'
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
    id = request.form.get('userid')
    password = request.form.get('password')
    cursor,connection=connectToDB()
    if request.method=='POST' and 'userid' in request.form and 'password' in request.form:
        mID = request.form.get('userid')
        pw = request.form.get('password')
        if "4444" in str(mID): #Broker
            cursor.execute(f"SELECT * FROM Brokers WHERE EID={mID};")
            option=1
        elif "5123" in str(mID): # Manager
            cursor.execute(f"SELECT * FROM Manager WHERE EID={mID};")
            option=2
        else: # Client
            cursor.execute(f"SELECT * FROM Clients WHERE ClientID={mID};")
            option=3
        acc = cursor.fetchone()
        if acc:
            session['loggedin']=True
            session['id'] = mID
            if option==2:
                if str(acc[1]) == str(pw):
                    session['name'] = 'manager'
                    return redirect(url_for('manager'))
                else:
                    invalid=True
                    msg='Invalid Password or ID'
            elif option==1:
                session['name'] = 'broker'
                pass
            elif option==3:
                session['name'] = 'client'
                pass
        else:
            msg+='\nunsuccessful'

    return render_template('login.html', title="Login",msg=msg,invalid=invalid)

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
    return render_template('manager.html',title="Manager",name=name,branch=branch)

@app.route('/brokersmanage')
def managebroker():
    return render_template('brokerformanager.html')

@app.route('/investment')
def investment():
    cursor, connection = connectToDB()
    cursor.execute("SELECT * FROM Investment;")
    data = []
    for vals in cursor.fetchall():
        data.append({"invID":vals[0],"invType":vals[1],"invName":vals[2],"invRA":vals[-1]})
    return render_template('inv.html',title="Investment", data=data)

@app.route('/addinv')
def addinv():
    return render_template('addinv.html')

@app.route('/broker')
def broker():
    return render_template('broker.html',title="Broker")

if __name__ == "__main__":
    app.run(port='8080', debug=True)