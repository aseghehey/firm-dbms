from crypt import methods
from flask import Flask, render_template, redirect, url_for, request
import sqlalchemy

app = Flask(__name__)
app.config['SECRET_KEY']='ghjhbkhcjgk,ghvuti12fk3'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:Matidrewe012403@localhost/investment_bank'

@app.route('/')
def home():
    title = 'Investment Bank'
    return render_template('base.html', title=title)

@app.route('/about')
def about():
    return render_template('about.html',title="About Us")

@app.route('/login', methods=['GET','POST'])
def login():
    id = request.form.get('userid')
    password = request.form.get('password')

    if not id or not password:
        err = "You left one or both of the fields blank"

    return render_template('login.html', title="Login",err=err)

if __name__ == "__main__":
    app.run(port='8080', debug=True)