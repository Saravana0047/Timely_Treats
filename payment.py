from flask import Flask, request, render_template

app = Flask(__name__)
app.secret_key = '8637473588'


@app.route('/process_payment', methods=['POST'])
def process_payment():
    payment_method = request.form.get('payment_method')  

    if payment_method is None:
        return "No payment method selected.", 400 

    if payment_method == 'UPI':
        
        upi_id = request.form.get('upi_id')
        if upi_id:
            return "UPI Payment successful!"
        else:
            return "Please enter a valid UPI ID."

    elif payment_method == 'Card':
        
        name = request.form.get('name')
        card_number = request.form.get('card_number')
        expiry_date = request.form.get('expiry_date')
        cvv = request.form.get('cvv')
        if name and card_number and expiry_date and cvv:
        
            return "Card Payment successful!"
        else:
            return "Please fill out all card details."

    elif payment_method == 'COD':
        
        return "Order placed successfully! You can pay in cash upon delivery."

    else:
        return "Invalid payment method selected."




    
@app.route('/process_payment')
def payment_get():
    return render_template('payment.html')
    
    
    
if __name__ == '__main__':
    app.run(debug=True)
