from flask import Flask, render_template, request, jsonify
import os
from utils import generate_description, extract_product_name, search_ebay

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'})

    file = request.files['image']
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    description = generate_description(filepath)
    product_name = extract_product_name(description)
    products = search_ebay(product_name)

    return jsonify({'description': description, 'products': products})

if __name__ == "__main__":
    app.run(debug=True)
