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
    # Simple password protection (change this!)
    return render_template('admin.html')

@app.route('/api/products', methods=['GET'])
def get_products():
    products = load_products()
    category = request.args.get('category')
    
    if category and category != 'all':
        products = [p for p in products if p.get('category') == category]
    
    # Sort by newest first
    products.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    return jsonify(products)

@app.route('/api/products', methods=['POST'])
def add_product():
    """Admin: Add new product"""
    data = request.json
    
    # Basic validation
    required = ['name', 'price', 'affiliate_link', 'image']
    if not all(k in data for k in required):
        return jsonify({'error': 'Missing required fields'}), 400
    
    new_product = {
        'id': str(uuid.uuid4()),
        'name': data['name'],
        'price': data['price'],
        'original_price': data.get('original_price', ''),
        'image': data['image'],
        'affiliate_link': data['affiliate_link'],
        'category': data.get('category', 'other'),
        'description': data.get('description', ''),
        'deal_type': data.get('deal_type', 'normal'),  # normal, lightning, hot
        'active': True,
        'created_at': datetime.now().isoformat()
    }
    
    products = load_products()
    products.append(new_product)
    save_products(products)
    
    return jsonify({'message': 'Product added successfully!', 'product': new_product}), 201

@app.route('/api/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Admin: Delete product"""
    products = load_products()
    products = [p for p in products if p['id'] != product_id]
    save_products(products)
    return jsonify({'message': 'Product deleted'}), 200

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get basic stats for admin"""
    products = load_products()
    return jsonify({
        'total_products': len(products),
        'categories': list(set(p.get('category', 'other') for p in products)),
        'active_deals': len([p for p in products if p.get('deal_type') != 'normal'])
    })

# Affiliate redirect tracker (optional - for analytics)
@app.route('/go/<product_id>')
def track_click(product_id):
    products = load_products()
    product = next((p for p in products if p['id'] == product_id), None)
    
    if product and product.get('active'):
        # Here you could log the click to a file/database
        return redirect(product['affiliate_link'])
    
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
