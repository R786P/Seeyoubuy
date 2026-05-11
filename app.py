import os
import json
import uuid
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Data file path
DATA_FILE = os.path.join('data', 'products.json')

# Ensure data directory exists
os.makedirs('data', exist_ok=True)

# Initialize JSON file if not exists
def init_db():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump([], f)

def load_products():
    init_db()
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_products(products):
    with open(DATA_FILE, 'w') as f:
        json.dump(products, f, indent=2)

# ============ ROUTES ============

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/api/products', methods=['GET'])
def get_products():
    products = load_products()
    category = request.args.get('category')
    
    if category and category != 'all':
        products = [p for p in products if p.get('category') == category]
    
    products.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    return jsonify(products)

@app.route('/api/products', methods=['POST'])
def add_product():
    """Admin: Add new product with multiple images"""
    data = request.json
    
    required = ['name', 'price', 'affiliate_link', 'images']
    if not all(k in data for k in required):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Ensure images is a list
    if isinstance(data['images'], str):
        images = [data['images']]
    else:
        images = data['images']
    
    new_product = {
        'id': str(uuid.uuid4()),
        'name': data['name'],
        'price': data['price'],
        'original_price': data.get('original_price', ''),
        'images': images,
        'affiliate_link': data['affiliate_link'],
        'category': data.get('category', 'other'),
        'description': data.get('description', ''),
        'deal_type': data.get('deal_type', 'normal'),
        'active': True,
        'created_at': datetime.now().isoformat()
    }
    
    products = load_products()
    products.append(new_product)
    save_products(products)
    
    return jsonify({'message': 'Product added successfully!', 'product': new_product}), 201

@app.route('/api/products/<product_id>', methods=['PUT'])
def update_product(product_id):
    """Admin: Update existing product with multiple images"""
    data = request.json
    products = load_products()
    
    for p in products:
        if p['id'] == product_id:
            updatable_fields = ['name', 'price', 'original_price', 'images',
                              'affiliate_link', 'category', 'description', 'deal_type', 'active']
            for field in updatable_fields:
                if field in data:  # ←←← FIXED: was "if field in"
                    if field == 'images':
                        if isinstance(data[field], str):
                            p[field] = [data[field]]
                        else:
                            p[field] = data[field]
                    else:
                        p[field] = data[field]
            p['updated_at'] = datetime.now().isoformat()
            save_products(products)
            return jsonify({'message': 'Product updated!', 'product': p}), 200
    
    return jsonify({'error': 'Product not found'}), 404

@app.route('/api/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    products = load_products()
    products = [p for p in products if p['id'] != product_id]
    save_products(products)
    return jsonify({'message': 'Product deleted'}), 200

@app.route('/api/stats', methods=['GET'])
def get_stats():
    products = load_products()
    return jsonify({
        'total_products': len(products),
        'categories': list(set(p.get('category', 'other') for p in products)),
        'active_deals': len([p for p in products if p.get('deal_type') != 'normal'])
    })

@app.route('/go/<product_id>')
def track_click(product_id):
    products = load_products()
    product = next((p for p in products if p['id'] == product_id), None)
    
    if product and product.get('active'):
        return redirect(product['affiliate_link'])
    
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
