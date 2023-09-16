from flask import Flask, render_template, request
import mysql.connector
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import json
from flask_mail import Mail, Message
import datetime
with open('config.json', 'r') as c:
    params = json.load(c)["params"]
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:arijit@localhost/coddingthunders'
db = SQLAlchemy(app)
class contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    message = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    email = db.Column(db.String(20), nullable=False)
class Posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(21), nullable=False)
    content = db.Column(db.String(120), nullable=False)
    img_file = db.Column(db.String(45), nullable=True)
    date = db.Column(db.String(12), nullable=True)
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
# @app.route("/")
# @app.route("/home")

# def home():
#     return render_template('index.html',params=params)


@app.route("/about")
def about():    
    return render_template('about.html',params=params)


@app.route("/contact", methods = ['GET','POST'])
def contact():
	if request.method =='POST':
		# '''d mm'''
		if(request.method=='POST'):
			'''Add entry to the database'''
			name = request.form.get('name')
			email = request.form.get('email')
			phone = request.form.get('num')
			date = request.form.get('date')
			message = request.form.get('message')
			entry = contacts(name=name, phone = phone, message = message, date= date,email = email )
			db.session.add(entry)
			db.session.commit()
			msg = Message('Hello', sender = params['gmail-user'], recipients = [email,params['gmail-user']]) 
			msg.body = "Hello Flask message sent from Flask-Mail" + f'\n{name}\n{phone}\n{date}\n{message}\n This mail is sent using flask app' + f'\n{phone}' + f'\n{email}'
			mail.send(msg)
	return render_template('contact.html',params=params)

#DELETE t1 FROM contacts t1  INNERJOIN contacts t2 WHERE t1.id < t2.id AND t1.email = t2.email;
 
@app.route("/post/<post_slug>", methods=['GET'])
def post_route(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template('blog.html', params=params, post=post)

@app.route("/")
def home():
    post = Posts.query.filter_by().all()[0:params['no_of_posts']]
    return render_template('index.html', params=params, posts=post)
@app.route("/signin")
def signin():
	return render_template('Signin Template · Bootstrap.html', params=params)
app.run(debug=True) 