from flask import Flask, request, render_template, url_for, redirect, flash
import mysql.connector
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.secret_key = '8637473588'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'timelytreats0047@gmail.com'
app.config['MAIL_PASSWORD'] = 'vlgk noli tszt psbz'
app.config['MAIL_DEFAULT_SENDER'] = 'timelytreats0047@gmail.com'



app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mypass'
app.config['MYSQL_DB'] = 'timely_treats_db'

mail = Mail(app)
s = URLSafeTimedSerializer('ThisIsSecretKey')

users_db = {'test@example.com': {'password': 'old_hashed_password'}}

db = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB'],
    auth_plugin='mysql_native_password'
)
cursor = db.cursor()

@app.route('/', methods=['GET', 'POST'])
def forget_password():
    if request.method == 'POST':
        email = request.form['username']
        cursor.execute("SELECT * FROM customer_details WHERE username = %s", (email,))
        user = cursor.fetchone()

        if user:
            token = s.dumps(email, salt='password-reset-salt')
            reset_link = url_for('reset_password', token=token, _external=True)

            msg = Message('Password Reset', recipients=[email])
            msg.body = f'Click this link to reset your password: {reset_link}'
            msg.html = f"""
                    <p> Click the link below to reset your password:<p>
                    <a href= "{reset_link}"> Click here to Reset Password</a>
                    <p>If you did not request this password reset, please ignore this mail.</p>
                """
            mail.send(msg)
            
            flash('A Reset link has been sent to your mail')
            return render_template('forget.html', token=token)
        
        else:
            return 'This email is not registered!'
    
    return render_template('forget.html')

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = s.loads(token, salt='password-reset-salt', max_age=3600)
    except:
        return 'The reset link is invalid or has expired.'

    if request.method == 'POST':
        new_password = request.form['password']
        con_password = request.form['conpassword']

        if new_password != con_password:
            return 'Password not Match'
        

        hashed_password = generate_password_hash(new_password)

        cursor.execute("UPDATE customer_details SET password = %s WHERE username = %s", (hashed_password, email))
        db.commit()
        return 'Your password has been reset successfully.'

    return render_template('newpass.html')
# def reset_password(token):
#     try:
#         email = s.loads(token, salt='password-reset-salt', max_age=3600)
#     except:
#         return 'The reset link is invalid or has expired.'

#     if request.method == 'POST':
#         new_password = request.form['conpassword']
#         users_db[email]['password'] = generate_password_hash(new_password)
#         return 'Your password has been reset successfully.'


#     if request.method == 'POST':
#         new_password = request.form['reset_token']

#         cursor.execute("UPDATE users SET password = %s WHERE email = %s", (generate_password_hash(new_password), email))
#         db.commit()
#         return 'Your password has been reset successfully.'

#     return render_template('reset_password.html')

if __name__ == '__main__':
    app.run(debug=True)


