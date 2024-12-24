# from flask import Flask, render_template, flash, redirect, url_for, request
# import pymysql
# from itsdangerous import URLSafeTimedSerializer
# from werkzeug.security import generate_password_hash, check_password_hash

# app = Flask(__name__)
# app.config['SECRET_KEY'] = '8637473588'

# db = pymysql.connect(
#     host="localhost",
#     user="root",
#     password="Shree@2002#30",
#     database="timely_treats_db",
#     auth_plugin='Shree@2002#30'
# )
# cursor = db.cursor()

# users = {'user@example.com': {'password': generate_password_hash('old_password')}}
# serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])


# @app.route('/', methods=['GET', 'POST'])
# def forget():
#     if request.method == 'POST':
#         email = request.form.get('email')

#         query = "SELECT * FROM customer_details WHERE username = %s"
#         cursor.execute(query, (email,))
#         customer = cursor.fetchone()
#         if customer:
           
#             token = serializer.dumps(email, salt='password-reset-salt')
#             reset_url = url_for('reset_token', token=token, _external=True)
#             flash(f'Password reset link: {reset_url}', 'info')
#             return redirect(url_for('forget'))
#         else:
#             flash('Email not found', 'danger')
#     return render_template('forget.html')


# @app.route('/reset/<token>', methods=['GET', 'POST'])
# def reset_token(token):
#     try:

#         email = serializer.loads(token, salt='password-reset-salt', max_age=900)
#     except Exception:
#         flash('Invalid or expired token', 'warning')
#         return redirect(url_for('forget'))

#     if request.method == 'POST':
#         new_password = request.form.get('password')
#         confirm_password = request.form.get('conpassword')

#         if new_password != confirm_password:
#             flash('Passwords do not match!', 'danger')
#         else:

#             users[email]['password'] = generate_password_hash(new_password)
#             flash('Your password has been updated!', 'success')
#             return redirect(url_for('login'))
    
#     return render_template('newpass.html')


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form.get('email')
#         password = request.form.get('password')

#         if not email or not password:
#             flash('Please fill out both fields', 'danger')
#         elif email in users and check_password_hash(users[email]['password'], password):
#             flash('Login successful', 'success')
#             return redirect(url_for('home'))
#         else:
#             flash('Invalid credentials', 'danger')

#     return render_template('login.html')


# @app.route('/home')
# def home():
#     return "Welcome to the homepage!"

# if __name__ == '__main__':
#     app.run(debug=True)


import smtplib

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('timelytreats0047@gmail.com', 'vlgk noli tszt psbz')
    print("Successfully connected to the SMTP server.")
    server.quit()
except Exception as e:
    print(f"Failed to connect: {e}")
