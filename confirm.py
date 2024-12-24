from flask import Flask, render_template
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)


EMAIL_ADDRESS = "timelytreats0047@gmail.com"
EMAIL_PASSWORD = "vlgk noli tszt psbz"
SMTP_SERVER = "smtp.gmail.com"  
SMTP_PORT = 587  

def send_confirmation_email(to_email, order_details):
    # Render the HTML template with order details
    email_content = render_template('order_confirmation_email.html', **order_details)

    msg = MIMEMultipart("alternative")
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg['Subject'] = "Order Confirmation - Timely Treats"

    # Attach HTML content to the email
    msg.attach(MIMEText(email_content, 'html'))

    # Send the email
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())



if __name__ == "__main__":
    app.run(debug=True)