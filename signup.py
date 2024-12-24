from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from flask_mail import Mail, Message
import mysql.connector
import uuid

app = Flask(__name__)
app.secret_key = '8637473588'

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'timelytreats0047@gmail.com'
app.config['MAIL_PASSWORD'] = 'vlgk noli tszt psbz'
app.config['MAIL_DEFAULT_SENDER'] = 'timelytreats0047@gmail.com'
mail = Mail(app)

# Configure MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mypass",
    database="timely_treats_db"
)

@app.route('/')
def enter():
    return render_template('signup.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        customer_name = request.form.get('customer_name')
        mobile = request.form.get('mobile')
        username = request.form.get('username')
        user_password = request.form.get('password')
        address = request.form.get('address')

        hashed_password = generate_password_hash(user_password, method='pbkdf2:sha256')

        cursor = db.cursor()
        # Generate a verification token
        token = str(uuid.uuid4())

        query = """INSERT INTO customer__details (customer_name, username, user_password, address, mobile, email_verification, verification_token)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        values = (customer_name, username, hashed_password, address, mobile, False, token)

        try:

            cursor.execute(query, values)
            db.commit()
            send_verification_email(username, token)
            

            return redirect(url_for('enter'))
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            db.rollback()
            return 'Check your mail for verification'

    return render_template('signup.html')

def send_verification_email(user_email, token):
    verification_link = f"http://localhost:5000/verify_email?token={token}"
    msg = Message('Email Verification', 
                  sender='timelytreats0047@gmail.com', 
                  recipients=[user_email])
    msg.body = f'Please click the link to verify your email: {verification_link}'
    mail.send(msg)

@app.route('/verify_email')
def verify_email():
    token = request.args.get('token')

    cursor = db.cursor()
    # Check if the token is valid
    token_query = "SELECT * FROM customer__details WHERE verification_token = %s AND email_verification = %s"
    cursor.execute(token_query, (token, False))
    user = cursor.fetchone()

    if user:
        update_query = "UPDATE customer__details SET email_verification = %s, verification_token = NULL WHERE verification_token = %s"
        cursor.execute(update_query, (True, token))
        db.commit()

        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)





# from flask import Flask, render_template, request, redirect, url_for
# from werkzeug.security import generate_password_hash
# import mysql.connector

# app = Flask(__name__)

# db = mysql.connector.connect(
#     host = "localhost",
#     user = "root",
#     password = "mypass",
#     database = "timely_treats_db"
# )

# @app.route('/')
# def enter():
#     return render_template('signup.html')

# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         customer_name = request.form.get('customer_name')
#         mobile = request.form.get('mobile')
#         username = request.form.get('username')
#         password = request.form.get('password')
#         address = request.form.get('address')

#         hashed_password = generate_password_hash(password)


#         cursor = db.cursor()
#         query = "INSERT INTO customer_details (customer_name,username, password, address, mobile) VALUES (%s, %s, %s, %s, %s)"
#         values = (customer_name,username, hashed_password, address, mobile)

#         try:
#             cursor.execute(query, values)
#             db.commit()
#             return render_template('login.html')
#         except mysql.connector.Error as err:
#             print(f"Error:{err}")
#             db.rollback()
    
#     return render_template('signup.html')

# @app.route('/success')
# def success():
#     return "signup Successfull"

# if __name__ == '__main__':
#     app.run(debug = True)
        