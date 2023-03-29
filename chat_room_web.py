from datetime import datetime
import re
import logging
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import openai
import chat_bot_api
from flask_mysqldb import MySQL
import MySQLdb.cursors

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s:%(levelname)s: %(message)s")
file_handler = logging.FileHandler("static/faileduser.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

app = Flask(__name__)

#used to assign session cookies/secure the cookies
app.secret_key = 'LetMeIn'
            
#This information will need to be updated for your personal stuff

#confinguring python to connect to the database
app.config['MYSQL_HOST'] = 
app.config['MYSQL_USER'] = 
app.config['MYSQL_PASSWORD'] = #left blank due to it being my personal password
app.config['MYSQL_DB'] = 
mysql = MySQL(app)


@app.route('/')
@app.route('/Kiel_Ott_Chat/login', methods=['GET', 'POST'])
def login():
    """the login method will allow you to enter you username and password
    and if it is stored in the database
    will allow you to access the rest of the pages"""

    message = "Please login"

    #if the username and password are entered it will query the database to see if they are saved
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s and passwords = %s',
        (username, password))
        
        account = cursor.fetchone()

        #using the session to confim login and allow access to webpages.
        #Session will restrict access if not logged in
        #will also log all failed attempts to log in
        if not account:
            logger.info("%s %s failed to log in", username, request.remote_addr)
            message = 'Incorrect username/password!'

        #starting session if your account exists
        else:
            logger.info("%s %s login successful", username, request.remote_addr)
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return redirect(url_for('index2'))


    return render_template('login.html', message=message)

@app.route('/Kiel_Ott_Chat/register', methods=['GET', 'POST'])
def register():
    """this method will allow the user to register their username
and password and check to make sure that they fall within specificed
parameters"""
    message="Please register to continue"

    #will just reload the register template
    if request.method == 'GET':
        return render_template('register.html')

    #pulling the information from the page and saving it in variables
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s',(username,))
        exists = cursor.fetchone()
        if exists:
            message = "that account already exists"
        #using regular expression to check username is valid
        elif not re.match(r'[A-Za-z0-9]*$', username):
            message= 'Username must contain only letters and numbers!'

        #checking any new registration against the list
        elif not check_list(password):
            message = "That is a commonly used password and is not valid!"

        #using password check function to make sure password is valid
        elif not password_check(password):
            message= ('The password must contain lowercase, uppercase, symbols,'
            'and numbers and be at least 12 characters long!')
            
        #if everything checks out it will save the informatin into the SQL database
        #will use SQL to insert the username and password into a running
        #database and redirect to login once registered
        else:
            #this cursor allows the actual interaction with the database
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s)', (username, password,))
            mysql.connection.commit()
            message = 'You have successfully registered!'
            return redirect(url_for('login'))

    #if username and password left blank it will request you fill in info
    elif request.method == 'POST':
        message= 'Please enter the required information!'
    return render_template('register.html', message=message)

@app.route('/Kiel_Ott_Chat/index2', methods=['GET', 'POST'])
def index2():
    
    if request.method == "POST" and 'loggedin' in session:
        prompt = request.form['prompt']
        res = {}
        
        res['answer'] = chat_bot_api.generateChatResponse(prompt)
        return jsonify(res), 200
        
    return render_template('index2.html')
                                             
@app.route('/Kiel_Ott_Chat/logout')
def logout():
    """this method will allow for log out and return to restricted access"""

    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)

    return redirect(url_for('login'))

def check_list(password):
    """This method will open and read the common password file and check
    any new password entered against it"""

    #opeing and reading file and closing it
    with open ("static/CommonPassword.txt", "r", encoding="utf-8") as f_read:
        reader = f_read.readlines()
        f_read.close()
        check = True

    #using a for loop to check the list
        for item in reader:
            if password == item.strip():
                check = False
    return check
def password_check(password):
    """This method will check that the password is within required specs"""

    len_error = len(password) < 12
    digit_error = re.search(r"\d", password) is None
    upper_error = re.search(r"[A-Z]", password) is None
    lower_error = re.search(r"[a-z]", password) is None
    symbol_error = re.search(r"\W", password) is None
    password_ok = not(len_error or digit_error or upper_error or
                      lower_error or symbol_error)

    return password_ok

if __name__== '__main__':
    app.run(debug=True, port=5000)
