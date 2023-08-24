from flask import Flask, render_template, request
import mysql.connector
# from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import json
from flask_mail import Mail, Message
with open('config.json', 'r') as c:
    params = json.load(c)["params"]
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/codding thrunder'
# db = SQLAlchemy(app)
myconn = mysql.connector.connect(host = "localhost", user = "root",passwd = "arijit",database="coddingthunders")  
cur = myconn.cursor()  

# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'password'
# app.config['MYSQL_DB'] = 'coddingthunders'
# class contacts(db.Model):
#     sno = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), nullable=False)
#     phone_number = db.Column(db.String(12), nullable=False)
#     msg = db.Column(db.String(120), nullable=False)
#     date = db.Column(db.String(12), nullable=False)
#     email = db.Column(db.String(20), nullable=False)
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
	MAIL_USE_TLS = False,
    MAIL_USERNAME = params['gmail-user'],
    MAIL_PASSWORD = params['gmail-password'],
	MAIL_DEFAULT_SENDER = params['gmail-user']
)
mail = Mail(app)
@app.route("/")
@app.route("/home")

def home():
    return render_template('index.html',params=params)


@app.route("/about")
def about():
    return render_template('about.html',params=params)


@app.route("/contact", methods = ['GET','POST'])
def contact():
	if request.method =='POST':
		# '''d mm'''
		name = request.form["name"]
		phone = request.form["num"]
		message = request.form["message"]
		date = request.form["date"]
		email = request.form["email"]
		# entry = contacts(name=name, phone_number = phone,date = date ,msg = message,email = email )
		# db.session.add(entry)
		# db.session.commit()
		# cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cur.execute("INSERT INTO contacts (name,phone,message,email) VALUES (%s,%s,%s,%s)",(name,phone,message,email))
		myconn.commit()
	# 	mail.send_message('New message from blog' + name,
    # sender = email,
    # recipients = [params['gmail-user']],
    # body = message + "\n" +phone ,)
		msg = Message('Hello', sender = params['gmail-user'], recipients = ['nandyarijit1610@gmail.com','annandy2002@gmail.com','berapriti727@gmail.com']) 
		msg.body = "Hello Flask message sent from Flask-Mail" + f'\n{name} This mail is sent using flask app' + f'\n{phone}' + f'\n{email}'
		mail.send(msg)
	return render_template('contact.html',params=params)


@app.route("/blog")
def blog_page():
	return render_template('blog.html',params=params)


app.run(debug=True)

