from flask import Flask, render_template, redirect, url_for, request
import mysql.connector

app = Flask(__name__)


db_config = {
    'host' : 'localhost',
    'user' : 'root',
    'password' : 'mypass',
    'database' : 'timely_treats_db',
    'auth_plugin' : 'mysql_native_password'
}

@app.route('/')
def items():
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT image_name, image_filename FROM items_images")
    products = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('items.html', products= products)

@app.route('/order/<int:id>')
def order_details(id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM items_images WHERE id = %s", (id,))
    product = cursor.fetchone()

    cursor.execute("SELECT * FROM inventory WHERE item_S_no = %s", (id,))
    item = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template('order.html', product=product, item=item)

@app.route('/place_order/<int:id>')
def place_order(id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM items_images WHERE id = %s", (id,))
    product = cursor.fetchone()

    cursor.execute("SELECT * FROM inventory WHERE item_S_no = %s", (id,))
    item = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template('side_nav.html', product=product, item=item)


if __name__ == '__main__':
    app.run(debug=True)
