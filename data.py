from flask import Flask, request, redirect, url_for
import mysql.connector
import os

app = Flask(__name__)

# Define the upload folder path
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Route to handle image upload
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return redirect(request.url)

    file = request.files['image']
    
    if file.filename == '':
        return redirect(request.url)

    if file:
        # Save the file locally (for storing file paths in DB)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Insert image path into the database
        insert_image_path(file_path)

        return 'Image Uploaded Successfully!'

# Example function to insert image path into database
def insert_image_path(image_path):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Shree@2002#30",
        database="images"
    )
    cursor = connection.cursor()

    query = "INSERT INTO images (4 sweets, C:\Users\SARAVANA\Downloads\4 sweets ss_11zon.jpg) VALUES (%s, %s)"
    cursor.execute(query, (os.path.basename(image_path), image_path))

    connection.commit()
    cursor.close()
    connection.close()

if __name__ == '__main__':
    app.run(debug=True)
