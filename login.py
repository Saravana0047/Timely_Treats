from flask import Flask, render_template, request, redirect, session, url_for, flash
from werkzeug.security import check_password_hash
import mysql.connector

app = Flask(__name__)
app.secret_key = '8637473588'

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mypass",
    database="timely_treats_db",
    auth_plugin='mysql_native_password'
)
cursor = db.cursor()

@app.route('/')
def enter():
    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['Username']
        password = request.form['Password']
        
        
        query = "SELECT * FROM customer__details WHERE username = %s"
        cursor.execute(query, (username,))
        customer = cursor.fetchone()

        
        
        if customer:
            db_customer_name = customer[1]
            # username = customer[2]     
            stored_hashed_password = customer[3]
            # session['customer_name'] = db_customer_name

            if check_password_hash(stored_hashed_password, password):
                session['customer_name'] = db_customer_name
                flash('Login successful!', 'success')
                return redirect(url_for('index'))
            else:
                return "Invalid credentials. Please try again."
        else:
            return 'Invalid username or password'
    
    return render_template('login.html')

@app.route('/home')
def index():
    customer_name = session.get('customer_name')
    if customer_name:
        return render_template('index.html', customer_name=customer_name)
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
# break------------------------------------------------>>>>>>>>>>>>>>>>>>>>









# from flask import Flask, request, render_template

# app = Flask(__name__)

# @app.route('/')
# def home():
#     return render_template('login.html')  

# @app.route('/login', methods=['POST'])
# def login():
#     if request.method == 'POST':
#         user = request.form.get('Username')
#         password = request.form.get('Password')
    
#         if user == 'saravana' and password == '1234':
#             return render_template('index.html') 
#         else:
#             return render_template()

# if __name__ == '__main__':
#     app.run(debug=True)


