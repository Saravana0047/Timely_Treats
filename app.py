from flask import Flask, render_template, request, redirect, session, url_for, flash, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
import uuid,smtplib, mysql.connector
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime


app = Flask(__name__)
app.secret_key = '8637473588'

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'mypass',
    'database': 'timely_treats_db',
    'auth_plugin': 'mysql_native_password'
}

# Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'timelytreats0047@gmail.com'
app.config['MAIL_PASSWORD'] = 'vlgk noli tszt psbz'
app.config['MAIL_DEFAULT_SENDER'] = 'timelytreats0047@gmail.com'

mail = Mail(app)
s = URLSafeTimedSerializer('ThisIsSecretKey')

# Function to get database connection
def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

@app.route('/')
def index():
    customer_id = session.get('customer_id')
    if not customer_id:
        return redirect(url_for('login'))
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)  # Use dictionary cursor

        categories = {
            "Mysore Pak": "SELECT id, Item_name, Image_fileName, stock FROM inventory WHERE Special = 'Mysore pak signature'",
            "Soan Papdi": "SELECT id, Item_name, Image_fileName, stock FROM inventory WHERE Special = 'soanpapdi signature'",
            "Burfi": "SELECT id, Item_name, Image_fileName, stock FROM inventory WHERE Special = 'Burfi signature'",
            "Milk Sweets": "SELECT id, Item_name, Image_fileName, stock FROM inventory WHERE Special = 'Milk signature'",
            "Halwa": "SELECT id, Item_name, Image_fileName, stock FROM inventory WHERE Special = 'halwa signature'",
            "Kaju Sweets": "SELECT id, Item_name, Image_fileName, stock FROM inventory WHERE Special = 'kaju signature'",
            "Mixture": "SELECT id, Item_name, Image_fileName, stock FROM inventory WHERE Special = 'mixture signature'"
        }

        category_results = {}
        for category, query in categories.items():
            cursor.execute(query)
            category_results[category] = [
                {
                    "id": row["id"],
                    "Item_name": row["Item_name"],
                    "Image_fileName": row["Image_fileName"],
                    "stock": row["stock"]
                }
                for row in cursor.fetchall()
            ]
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        category_results = {key: [] for key in categories.keys()}
    finally:
        cursor.close()
        conn.close()

    return render_template('index.html', category_results=category_results)


@app.route('/home-index')
def home2():
    customer_id = session.get('customer_id')
    if not customer_id:
        return redirect(url_for('login'))
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)  # Use dictionary cursor

        categories = {
            "Mysore Pak": "SELECT id, Item_name, Image_fileName, stock FROM inventory WHERE Special = 'Mysore pak signature'",
            "Soan Papdi": "SELECT id, Item_name, Image_fileName, stock FROM inventory WHERE Special = 'soanpapdi signature'",
            "Burfi": "SELECT id, Item_name, Image_fileName, stock FROM inventory WHERE Special = 'Burfi signature'",
            "Milk Sweets": "SELECT id, Item_name, Image_fileName, stock FROM inventory WHERE Special = 'Milk signature'",
            "Halwa": "SELECT id, Item_name, Image_fileName, stock FROM inventory WHERE Special = 'halwa signature'",
            "Kaju Sweets": "SELECT id, Item_name, Image_fileName, stock FROM inventory WHERE Special = 'kaju signature'",
            "Mixture": "SELECT id, Item_name, Image_fileName, stock FROM inventory WHERE Special = 'mixture signature'"
        }

        category_results = {}
        for category, query in categories.items():
            cursor.execute(query)
            category_results[category] = [
                {
                    "id": row["id"],
                    "Item_name": row["Item_name"],
                    "Image_fileName": row["Image_fileName"],
                    "stock": row["stock"]
                }
                for row in cursor.fetchall()
            ]
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        category_results = {key: [] for key in categories.keys()}
    finally:
        cursor.close()
        conn.close()

    return render_template('index.html', category_results=category_results)


@app.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['Username']
        user_password = request.form['Password']

        session['username'] = username
        
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM customer__details WHERE username = %s"
        cursor.execute(query, (username,))
        customer = cursor.fetchone()
        
        conn.close()

        if customer:
            
            db_customer_name = customer[1]
            stored_hashed_password = customer[3]

            if check_password_hash(stored_hashed_password, user_password):
                
                session['customer_name'] = db_customer_name
                flash('Login successful!', 'success')


                session['customer_id'] = customer[0]  

                return redirect(url_for('home'))
            else:
                flash('Invalid password. Please try again.', 'error')
                return redirect(url_for('login'))  
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('login')) 

    return render_template('login.html')


@app.route('/home')
def home():
    customer_id = session.get('customer_id')

    if not customer_id:
        return redirect(url_for('login'))

    cart_items_dict = []
    category_results = {}
    customer_name = session.get('customer_name')

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                customer_cart.cart_id,
                customer_cart.item_id, 
                customer_cart.quantity, 
                customer_cart.item_price,
                customer_cart.item_name,
                inventory.item_type,
                inventory.Image_fileName,
                inventory.id, 
                inventory.Item_name  
            FROM 
                customer_cart 
            JOIN 
                inventory ON customer_cart.item_id = inventory.id
            WHERE 
                customer_cart.customer_id = %s
        """, (customer_id,))

        cart_items = cursor.fetchall()

        for item in cart_items:
            item['total_price'] = item['quantity'] * item['item_price']
            cart_items_dict.append({
                "cart_id": item['cart_id'], 
                "item_name": item['item_name'], 
                "item_price": item['item_price'], 
                "quantity": item['quantity'],
                "total_price": item['total_price'],
                "Image_fileName": item['Image_fileName'],
                "item_type": item['item_type']
            })

        categories = {
            "Mysore Pak": "SELECT id, Item_name, Image_fileName, stock FROM inventory WHERE Special = 'Mysore pak signature'",
            "Soan Papdi": "SELECT id, Item_name, Image_fileName, stock FROM inventory WHERE Special = 'soanpapdi signature'",
            "Burfi": "SELECT id, Item_name, Image_fileName, stock FROM inventory WHERE Special = 'Burfi signature'",
            "Milk Sweets": "SELECT id, Item_name, Image_fileName, stock FROM inventory WHERE Special = 'Milk signature'",
            "Halwa": "SELECT id, Item_name, Image_fileName, stock FROM inventory WHERE Special = 'halwa signature'",
            "Kaju Sweets": "SELECT id, Item_name, Image_fileName, stock FROM inventory WHERE Special = 'kaju signature'",
            "Mixture": "SELECT id, Item_name, Image_fileName, stock FROM inventory WHERE Special = 'mixture signature'"
        }

        for category, query in categories.items():
            cursor.execute(query)
            category_results[category] = [
                {
                    "id": row["id"],
                    "Item_name": row["Item_name"],
                    "Image_fileName": row["Image_fileName"],
                    "stock": row["stock"]
                }
                for row in cursor.fetchall()
            ]

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        category_results = {key: [] for key in categories.keys()} 
    finally:
        cursor.close()
        conn.close()

    return render_template(
        'home.html',
        customer_name=customer_name,
        cart_items=cart_items_dict,
        category_results=category_results
    )

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        customer_name = request.form.get('customer_name')
        mobile = request.form.get('mobile')
        username = request.form.get('username')
        user_password = request.form.get('password')
        address = request.form.get('address')
        hashed_password = generate_password_hash(user_password, method='pbkdf2:sha256')
        token = str(uuid.uuid4())

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """INSERT INTO customer__details (customer_name, username, user_password, address, mobile, email_verification, verification_token)
                       VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            values = (customer_name, username, hashed_password, address, mobile, False, token)
            cursor.execute(query, values)
            conn.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            if conn.is_connected():
                conn.rollback()
            return 'An error occurred during signup.'
        finally:
        
            cursor.close()
            conn.close()

        send_verification_email(username, token)
        return redirect(url_for('signup'))

    return render_template('signup.html')

def send_verification_email(user_email, token):
    verification_link = f"http://localhost:5000/verify_email?token={token}"
    msg = Message('Email Verification', sender='timelytreats0047@gmail.com', recipients=[user_email])
    msg.body = f'Please click the link to verify your email: {verification_link}'
    mail.send(msg)

@app.route('/verify_email')
def verify_email():
    token = request.args.get('token')
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        token_query = "SELECT * FROM customer__details WHERE verification_token = %s AND email_verification = %s"
        cursor.execute(token_query, (token, False))
        user = cursor.fetchone()

        
        cursor.fetchall()

        if user:
            update_query = "UPDATE customer__details SET email_verification = %s, verification_token = NULL WHERE verification_token = %s"
            cursor.execute(update_query, (True, token))
            conn.commit()
            return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))
    finally:
        cursor.close()
        conn.close()

# <------------Forget And Reset Password -------------->#

@app.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    if request.method == 'POST':
        email = request.form['username']

        # Use the connection function
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customer__details WHERE username = %s", (email,))
        user = cursor.fetchall()
        cursor.close()
        conn.close()

        if user:
            token = s.dumps(email, salt='password-reset-salt')
            reset_link = url_for('reset_password', token=token, _external=True)

            msg = Message('Password Reset', recipients=[email])
            msg.body = f'Click this link to reset your password: {reset_link}'
            msg.html = f"""
                <p>Click the link below to reset your password:</p>
                <a href="{reset_link}">Click here to Reset Password</a>
                <p>If you did not request this password reset, please ignore this mail.</p>
            """
            mail.send(msg)
            
            flash('A Reset link has been sent to your email.')
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
            flash('Passwords do not match. Please try again.')
            return render_template('newpass.html')

        hashed_password = generate_password_hash(new_password)

        try:
            # Use the connection function
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE customer__details SET user_password = %s WHERE username = %s", (hashed_password, email))
            conn.commit()
            cursor.close()
            conn.close()
            flash('Your password has been reset successfully.')
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            if conn.is_connected():
                conn.rollback()
                cursor.close()
                conn.close()
            return 'An error occurred while resetting your password.'

    return render_template('newpass.html')


# <-------- Items Page --------->


@app.route('/items.html')
def items():
    customer_name = session.get('customer_name')

    if not customer_name:
        return redirect(url_for('login'))

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Fetch sweets

        cursor.execute("SELECT * FROM inventory WHERE stock = 0")
        out_of_stock_items = cursor.fetchall()

        cursor.execute("""
        SELECT id, Item_name, Image_fileName, stock 
        FROM inventory 
        WHERE stock > 1 AND item_type = 'Sweets'
        """)
        sweets = [
        {
            "id": row["id"],
            "Item_name": row["Item_name"],
            "Image_fileName": row["Image_fileName"],
            "stock": row["stock"]
        }
        for row in cursor.fetchall()
        ]


        # Fetch savories
        cursor.execute("""
            SELECT id, Item_name, Image_fileName, stock 
            FROM inventory WHERE item_type = 'Savories'
        """)
        savories = [
            {
                "id": row["id"],
                "Item_name": row["Item_name"],
                "Image_fileName": row["Image_fileName"],
                "stock": row["stock"]
            }
            for row in cursor.fetchall()
        ]

        print("Sweets:", sweets)
        print("Savories:", savories)

    except mysql.connector.Error as err:
        print(f"Error: {err}") 
        sweets, savories = [], []
    finally:
        cursor.close()
        conn.close()

    customer_id = session.get('customer_id')
    cart_items_dict = []

    if customer_id:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                customer_cart.cart_id,
                customer_cart.item_id, 
                customer_cart.quantity, 
                customer_cart.item_price,
                customer_cart.item_name,
                inventory.item_type,
                inventory.Image_fileName
            FROM 
                customer_cart 
            JOIN 
                inventory ON customer_cart.item_id = inventory.id
            WHERE 
                customer_cart.customer_id = %s
        """, (customer_id,))

        cart_items = cursor.fetchall()
        cursor.close()

        if not cart_items:
            print("No items found in cart for customer_id:", customer_id)

        for item in cart_items:
            item['total_price'] = item['quantity'] * item['item_price']
            cart_items_dict.append({
                "cart_id": item["cart_id"], 
                "item_name": item["item_name"], 
                "item_price": item["item_price"], 
                "quantity": item["quantity"],
                "total_price": item["total_price"],
                "Image_fileName": item["Image_fileName"],
                "item_type": item["item_type"]
            })

    print("Customer ID from session:", customer_id)

    # Render template with data
    return render_template(
        'items.html',
        sweets=sweets,
        savories=savories,
        customer_name=customer_name,
        cart_items=cart_items_dict,
        out_of_stock_items=out_of_stock_items
    )


@app.route('/order/<int:id>')
def order_details(id):
    try:
        print(f"Fetching order details for ID: {id}")

        # Connect to database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM inventory WHERE id = %s", (id,))
        item = cursor.fetchone()
        if not item:
            print(f"No item found with ID: {id}")
            item = {}

        # Determine product details (fallback if needed)
        product = {
            "Image_fileName": item.get("Image_fileName", ""),
            "Item_name": item.get("Item_name", "")
        }

        # Fetch sweets and savories
        cursor.execute("SELECT id, Item_name, Image_fileName, stock FROM inventory WHERE item_type = 'Sweets' AND stock > 0")
        sweets = cursor.fetchall()

        cursor.execute("SELECT id, Item_name, Image_fileName, stock FROM inventory WHERE item_type = 'Savories' AND stock > 0")
        savories = cursor.fetchall()

        # Initialize category results
        category_results = {}

        # Fetch categories dynamically
        categories = {
            "Mysore Pak": "Mysore pak signature",
            "Soan Papdi": "soanpapdi signature",
            "Burfi": "Burfi signature",
            "Milk Sweets": "Milk signature",
            "Halwa": "halwa signature",
            "Kaju Sweets": "kaju signature",
            "Mixture": "mixture signature"
        }

        for category, special in categories.items():
            cursor.execute("SELECT id, Item_name, Image_fileName, stock FROM inventory WHERE Special = %s", (special,))
            category_results[category] = cursor.fetchall()

        # Fetch customer cart details
        customer_id = session.get('customer_id')
        print(f"Customer ID from session: {customer_id}")

        cart_items_dict = []
        if customer_id:
            cursor.execute("""
                SELECT 
                    customer_cart.cart_id,
                    customer_cart.item_id, 
                    customer_cart.quantity, 
                    customer_cart.item_price,
                    customer_cart.item_name,
                    inventory.item_type,
                    inventory.Image_fileName
                FROM 
                    customer_cart 
                JOIN 
                    inventory ON customer_cart.item_id = inventory.id
                WHERE 
                    customer_cart.customer_id = %s
            """, (customer_id,))
            cart_items = cursor.fetchall()

            for cart_item in cart_items:
                cart_items_dict.append({
                    "cart_id": cart_item["cart_id"],
                    "item_name": cart_item["item_name"],
                    "item_price": cart_item["item_price"],
                    "quantity": cart_item["quantity"],
                    "total_price": cart_item["quantity"] * cart_item["item_price"],
                    "Image_fileName": cart_item["Image_fileName"],
                    "item_type": cart_item["item_type"]
                })

    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        item = {}
        product = {}
        sweets = []
        savories = []
        category_results = {key: [] for key in categories.keys()}
        cart_items_dict = []
    finally:
        # Ensure cursor and connection are closed
        if cursor:
            cursor.close()
        if conn:
            conn.close()

        # Render the template
        return render_template(
            'order.html',
            product=product,
            item=item,
            sweets=sweets,
            savories=savories,
            cart_items=cart_items_dict,
            category_results=category_results
        )

# except Exception as e:
#         print(f"Error occurred: {e}")
#         return f"An error occurred: {str(e)}", 500


@app.route('/summary', methods=['POST', 'GET'])
def summary():

    item_id = request.form.get('item_id', '')
    item_name = request.form.get('item_name', '')
    item_price_str = request.form.get('item_price', '0')
    item_image = request.form.get('item_image', '')
    item_Type = request.form.get('item_Type', '')  
    quantity_str = request.form.get('quantity', '1')
    
    try:
        item_price = float(item_price_str)
    except ValueError:
        item_price = 0.0

    try:
        quantity = int(quantity_str)
    except ValueError:
        quantity = 1 

    total_amount = item_price * quantity
    

    return render_template('summary.html', item_id=item_id, item_name=item_name, item_price=item_price,
                           quantity=quantity, total_amount=total_amount, item_image=item_image, item_Type=item_Type)


@app.route('/summary_2')
def summary_2():
    customer_id = session.get('customer_id')

    print("Customer ID from session:", customer_id)

    if customer_id:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True) 
        cursor.execute("""
            SELECT 
                customer_cart.cart_id,
                customer_cart.item_id, 
                customer_cart.quantity, 
                customer_cart.item_price,
                customer_cart.item_name,
                inventory.item_type,
                inventory.Image_fileName,
                inventory.id, 
                inventory.Item_name  
            FROM 
                customer_cart 
            JOIN 
                inventory ON customer_cart.item_id = inventory.id
            WHERE 
                customer_cart.customer_id = %s
        """, (customer_id,))

        cart_items = cursor.fetchall()
        cursor.close()

        if not cart_items:
            print("No items found in cart for customer_id:", customer_id)

        cart_items_dict = []
        for item in cart_items:
            item['total_price'] = item['quantity'] * item['item_price']
            cart_items_dict.append({
                "cart_id": item['cart_id'], 
                "item_name": item['item_name'], 
                "item_price": item['item_price'], 
                "quantity": item['quantity'],
                "total_price": item['total_price'],
                "Image_fileName": item['Image_fileName'],
                "item_type": item['item_type']
            })

        return render_template('summary_cart.html', cart_items=cart_items_dict)
    else:
        return redirect('/login')



@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    
    customer_id = request.form.get('customer_id')
    item_id = request.form.get('item_id')
    item_name = request.form.get('item_name')
    item_price = request.form.get('item_price')
    quantity= request.form.get('quantity')
    category= request.form.get('type')
    
    
    print("Form Data: ", request.form)
    print(f"customer_id: {customer_id}, item_id: {item_id}, item_name: {item_name}, item_price: {item_price}, quantity: {quantity}, item_type: {category}")
    
    
    if customer_id and item_id and item_name and item_price and quantity and category:

        added_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db = get_db_connection()
        if not db:
            print("Failed to connect to the database!")
            return redirect(url_for('view_cart'))
        
        cursor = db.cursor()
        try:
            query = """
                INSERT INTO customer_cart (customer_id, item_id, item_name, category, quantity, item_price, added_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            values = (customer_id, item_id, item_name, category, quantity, item_price, added_date)
            cursor.execute(query, values)
            db.commit()

            
            flash("Item Added to Cart")
            print("Item added to cart successfully!")
        except Exception as e:
            db.rollback()  
            print(f"Error adding item to cart: {str(e)}")
        finally:
            cursor.close()
            db.close()
        
        return redirect(url_for('order_details', id=item_id))
    
    return "Error: Missing required fields or invalid data."


@app.route('/update_cart', methods=['POST'])
def update_cart():
    data = request.get_json()
    cart_id = data.get('cart_id')
    quantity = data.get('quantity')

    if not cart_id or not quantity:
        return jsonify({"success": False, "message": "Invalid input"})

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Update the quantity for the specific cart item
        update_query = "UPDATE customer_cart SET quantity = %s WHERE cart_id = %s"
        cursor.execute(update_query, (quantity, cart_id))
        conn.commit()
        return jsonify({"success": True, "message": "Cart updated successfully"})
    except Exception as e:
        print(e)
        return jsonify({"success": False, "message": "Database error"})
    finally:
        cursor.close()
        conn.close()


@app.route('/cart')
def view_cart():
    customer_id = session.get('customer_id')

    print("Customer ID from session:", customer_id)

    if customer_id:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True) 
        cursor.execute("""
            SELECT 
                customer_cart.cart_id,
                customer_cart.item_id, 
                customer_cart.quantity, 
                customer_cart.item_price,
                customer_cart.item_name,
                customer_cart.category,
                inventory.item_type,
                inventory.Image_fileName,
                inventory.id, 
                inventory.Item_name  
            FROM 
                customer_cart 
            JOIN 
                inventory ON customer_cart.item_id = inventory.id
            WHERE 
                customer_cart.customer_id = %s
        """, (customer_id,))

        cart_items = cursor.fetchall()
        cursor.close()

        if not cart_items:
            print("No items found in cart for customer_id:", customer_id)

        cart_items_dict = []
        for item in cart_items:
            item['total_price'] = item['quantity'] * item['item_price']
            cart_items_dict.append({
                "cart_id": item['cart_id'], 
                "item_name": item['item_name'], 
                "item_price": item['item_price'], 
                "quantity": item['quantity'],
                "total_price": item['total_price'],
                "image_filename": item['Image_fileName'],
                "item_type": item['item_type']
            })

            # Calculate total price for each item
            total_price = 0
    total_price = 0
    for item in items:
        item["total_price"] = item["quantity"] * item["price_per_unit"]
        total_price += item["total_price"]

        return render_template('cart.html', cart_items=cart_items_dict)
    else:
        return redirect('/login')

@app.route('/remove/<int:cart_id>', methods=['GET'])
def remove(cart_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM customer_cart WHERE cart_id = %s", (cart_id,))
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Item removed successfully!'})


@app.route('/my_order', methods=['POST'])
def my_order():
    # Get form data
    item_id = request.form.get('item_id')
    item = request.form.get('item')
    order_category = request.form.get('order_category')
    price_per_quantity = request.form.get('price_per_quantity')
    quantity = request.form.get('quantity')

    
    customer_id = session.get('customer_id')

    
    if not all([customer_id, item, price_per_quantity, quantity]):
        return "Error: Missing required fields or invalid data."


    item_id = int(item_id)


    db = get_db_connection()
    if not db:
        return redirect(url_for('view_cart'))

    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM customer__details WHERE customer_ID = %s", (customer_id,))
        customer = cursor.fetchone()

        if not customer:
            return "Error: Customer ID does not exist in the database."


        gst_percentage = 18
        total_gst = (int(quantity) * float(price_per_quantity) * gst_percentage) / 100
        gross_total = (int(quantity) * float(price_per_quantity)) + total_gst

        print("total_gst:",total_gst, "gross_total:", gross_total)
        query = """
        INSERT INTO order_details 
        (Item, item_id, order_category, quantity, price_per_quanity, total_gst, gross_total, Customer_ID)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (item, item_id, order_category, quantity, price_per_quantity, total_gst, gross_total, customer_id)
        cursor.execute(query, values)
        db.commit()

        flash("Item Added to order")
    except Exception as e:
        db.rollback()
        return f"Error adding item to order: {str(e)}"
    finally:
        cursor.close()
        db.close()

    return redirect(url_for('summary'))

    
@app.route('/view_order')
def view_order():
    customer_id = session.get('customer_id')
    if not customer_id:
        return redirect(url_for('login'))

    db = get_db_connection()
    if not db:
        return redirect(url_for('view_cart'))

    cursor = db.cursor()
    try:
        
        cursor.execute("""
            SELECT * FROM order_details
            WHERE customer_id = %s
        """, (customer_id,))
        orders = cursor.fetchall()

        print("Orders", orders)

        if not orders:
            return "No orders found for this customer."

        return render_template('my_order.html', orders=orders)

    except Exception as e:
        return f"Error fetching order details: {str(e)}"
    finally:
        cursor.close()
        db.close()

@app.route('/place_order', methods=['POST'])
def place_order():
    customer_id = session.get('customer_id')
    if customer_id:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT item_id, quantity FROM customer_cart WHERE customer_id = %s", (customer_id,))
        cart_items = cursor.fetchall()

        for item in cart_items:
            item_id, quantity = item

            cursor.execute("SELECT category, price FROM inventory WHERE item_id = %s", (item_id,))
            item_details = cursor.fetchone()
            if item_details:
                category, price_per_quantity = item_details

                total_gst = quantity * price_per_quantity * 18 % 100  
                gross_total = (quantity * price_per_quantity) + total_gst

                cursor.execute("""
                    INSERT INTO order_details 
                        (customer_id, item_id, order_category, quantity, price_per_quantity, total_gst, gross_total, order_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
                """, (customer_id, item_id, category, quantity, price_per_quantity, total_gst, gross_total))

        
        cursor.execute("DELETE FROM customer_cart WHERE customer_id = %s", (customer_id,))
        mysql.connection.commit()
        cursor.close()

        return redirect('/my_order')
    else:
        return redirect('/login')

# <------- Payment --------->

@app.route('/process_payment', methods=['POST'])
def process_payment():
    if request.method == 'POST':
        # Retrieve address details
        name = request.form.get('fullname')
        address = request.form.get('address')
        pincode = request.form.get('pincode')
        city = request.form.get('city')
        state = request.form.get('state')
        email = request.form.get('email')
        payment_method = request.form.get('payment_method')

        # Validate input
        if not (name and address and pincode and city and state and email and payment_method):
            return "Please fill in all required fields."

        print(f"Received data: Name={name}, Address={address}, Pincode={pincode}, City={city}, State={state}, Email={email}")

        # Order details to include in the email
        order_details = {
            "name": name,
            "address": address,
            "pincode": pincode,
            "city": city,
            "state": state,
            "email": email,
            "payment_method": payment_method
        }

        # Handle payment methods
        if payment_method == 'UPI':
            upi_id = request.form.get('upi_id')
            if not upi_id:
                return "Please enter a valid UPI ID."
        elif payment_method == 'Card':
            card_name = request.form.get('name')
            card_number = request.form.get('card_number')
            expiry_date = request.form.get('expiry_date')
            cvv = request.form.get('cvv')
            if not all([card_name, card_number, expiry_date, cvv]):
                return "Please fill out all card details."
        elif payment_method == 'COD':
            pass
        else:
            return "Invalid payment method selected."

        # Send confirmation email
        send_confirmation_email(email, order_details)
        return render_template('payment.html', success=True)

    
    # Order confirmation Mail 

def send_confirmation_email(to_email, order_details):
    
    customer_id = session.get('customer_id')
    print("Customer ID from session:", customer_id)

    gross_total = 0

    if customer_id:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                customer_cart.cart_id,
                customer_cart.item_id, 
                customer_cart.quantity, 
                customer_cart.item_price,
                customer_cart.item_name,
                customer_cart.category,
                inventory.item_type,
                inventory.Image_fileName,
                inventory.id, 
                inventory.Item_name  
            FROM 
                customer_cart 
            JOIN 
                inventory ON customer_cart.item_id = inventory.id
            WHERE 
                customer_cart.customer_id = %s
        """, (customer_id,))

        cart_items = cursor.fetchall()
        cursor.close()

        if not cart_items:
            print("No items found in cart for customer_id:", customer_id)

        cart_items_dict = []

        for item in cart_items:
            item['total_price'] = item['quantity'] * item['item_price']
            gross_total += item['total_price']
            cart_items_dict.append({
                "cart_id": item['cart_id'], 
                "item_name": item['item_name'], 
                "item_price": item['item_price'], 
                "quantity": item['quantity'],
                "total_price": item['total_price'],
                "image_filename": item['Image_fileName'],
                "item_type": item['item_type']
            })

    if isinstance(order_details, list):
        for item in order_details:
            item["total_price"] = item["quantity"] * item["item_price"]
            gross_total += item["total_price"]
    else:
        print("Error: order_details is not a list of dictionaries")

    print(f"\nGross Total: ₹{gross_total:.2f}")

    try:
        print("Order details for email:", order_details)
        email_content = render_template('mail.html', 
                                name=order_details["name"],
                                address=order_details["address"],
                                city=order_details["city"],
                                state=order_details["state"],
                                pincode=order_details["pincode"],
                                cart_items=cart_items,
                                gross_total=gross_total)

        
        if email_content is None:
            print("Template rendering failed: con-mail.html returned None.")
            return
        
        msg = Message(
            subject="Order Confirmation - Timely Treats",
            sender=app.config['MAIL_DEFAULT_SENDER'],
            recipients=[to_email]
        )
        msg.html = email_content

        mail.send(msg)
        print("Order confirmation email sent successfully.")

    except Exception as e:
        print(f"Error sending email: {e}")



# Contact

@app.route('/contact.html')
def contact():
    customer_name = session.get('customer_name')

    return render_template ('contact.html', customer_name=customer_name)

# privacy & policy
@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/terms&conditions')
def terms():
    return render_template('terms.html')

# Logout

@app.route('/logout')
def admin_logout():
    session.pop('logged_in', None)
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))

if __name__ == "__main__":
        app.run(host='0.0.0.0', port=5000, debug=True)
