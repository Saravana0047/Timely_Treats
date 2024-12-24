from flask import Flask, request, redirect, url_for, session, render_template, flash
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

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

# Function to get database connection
def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

@app.route('/')
def index():
    return redirect(url_for('admin_login'))

# Admin login route
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('Username')
        password = request.form.get('Password')

        if not username or not password:
            flash('Please enter both username and password.', 'danger')
            return redirect(url_for('admin_login'))

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_password FROM admin_use WHERE username = %s", (username,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result and check_password_hash(result[0], password):
            session['admin_logged_in'] = True
            flash('Login successful', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('adminlog.html')

# Admin dashboard route
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'admin_logged_in' not in session:
        flash("You need to log in first.", 'warning')
        return redirect(url_for('admin_login'))

    conn = get_db_connection()
    if conn is None:
        flash("Could not connect to the database.", 'danger')
        return redirect(url_for('admin_login'))

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventory")
    inventory_data = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('admin_dashboard.html', inventory=inventory_data)


@app.route('/add_item', methods=['POST'])
def add_item():
    if 'admin_logged_in' not in session:
        flash("You need to log in first.", 'warning')
        return redirect(url_for('admin_login'))

    item_name = request.form.get('item_name')
    quantity = request.form.get('quantity')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO inventory (item_name, stock) VALUES (%s, %s)", (item_name, quantity))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Item added successfully', 'success')
    return redirect(url_for('admin_dashboard'))

# Route to update the quantity of an item in the inventory
@app.route('/update_item', methods=['POST'])
def update_item():
    if 'admin_logged_in' not in session:
        flash("You need to log in first.", 'warning')
        return redirect(url_for('admin_login'))

    item_id = request.form.get('item_id')
    quantity = request.form.get('quantity')

    if not quantity.isdigit():
        flash("Please enter a valid quantity.", 'danger')
        return redirect(url_for('admin_dashboard'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE inventory SET stock = %s WHERE item_S_no = %s", (quantity, item_id))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Item quantity updated successfully', 'success')
    return redirect(url_for('admin_dashboard'))


# Route to delete an item from the inventory
@app.route('/delete_item', methods=['POST'])
def delete_item():
    if 'admin_logged_in' not in session:
        flash("You need to log in first.", 'warning')
        return redirect(url_for('admin_login'))

    item_id = request.form.get('item_id')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM inventory WHERE item_S_no = %s", (item_id,))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Item deleted successfully', 'success')
    return redirect(url_for('admin_dashboard'))

# Admin logout route
@app.route('/admin_logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash('Logged out successfully', 'success')
    return redirect(url_for('admin_login'))

if __name__ == "__main__":
    app.run(debug=True)