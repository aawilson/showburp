from __future__ import print_function
from __future__ import unicode_literals

import os

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Flask
from flask import flash, render_template, request, session, redirect
from sqlalchemy.orm import sessionmaker
from tabledef import *


engine = create_engine('sqlite:///tutorial.db', echo=True)

app = Flask(__name__)
app.config['PIPE_EMAILS_TO'] = 'email.out'


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "You're here!!  <a href='/logout'>Logout</a>"


@app.route('/login', methods=['POST'])
def do_login():

    username = str(request.form['username'])
    password = str(request.form['password'])

    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([username]), User.password.in_([password]))
    result = query.first()
    if result:
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return redirect('')


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect('')


@app.route('/lost_password', methods=['GET'])
def lost_password():
    return render_template('lost_password.html')


@app.route('/lost_password', methods=['POST'])
def do_lost_password():
    username = str(request.form['username'])
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([username]))
    result = query.first()

    if not result:
        flash('that user does not exist!')
        return lost_password()

    html_content = render_template('lost_password.email.html', username=username)

    text_part = MIMEText('ignore this', 'plain')
    html_part = MIMEText(html_content, 'html')

    email_msg = MIMEMultipart('alternative')
    email_msg['Subject'] = 'Password Reset!'
    email_msg['From'] = 'noreply@example.com'
    email_msg['To'] = result.email

    email_msg.attach(text_part)
    email_msg.attach(html_part)

    email_as_bytes = bytes(email_msg.as_string(), "utf8")

    with open(app.config['PIPE_EMAILS_TO'], 'ab') as f:
        f.write(email_as_bytes)

    flash('sent!')
    return redirect('')


@app.route('/reset_password/<string:username>', methods=['GET'])
def reset_password(username):
    return "Ok! Resetting that for sure, you'll get an email!"
    # We're not actually sending an email because that's not the point


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=4000)
