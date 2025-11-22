from flask import Flask, jsonify, request, render_template
from apig_wsgi import make_lambda_handler
import db
import os

app = Flask(__name__)

# --- Routes ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stocks', methods=['GET'])
def get_stocks():
    stocks = db.get_all_stocks()
    return jsonify(stocks)

@app.route('/api/stocks', methods=['POST'])
def add_stock():
    data = request.json
    symbol = data.get('symbol', '').upper()
    
    if not symbol:
        return jsonify({'error': 'Symbol is required'}), 400
    
    stock, error = db.add_stock(symbol)
    if error:
        return jsonify({'error': error}), 400
    
    return jsonify({'message': f'Stock {symbol} added', 'stock': stock})

@app.route('/api/stocks/<symbol>/star', methods=['POST'])
def toggle_star(symbol):
    new_status, error = db.toggle_star(symbol)
    if error:
        status_code = 404 if "not found" in error else 500
        return jsonify({'error': error}), status_code
    
    return jsonify({'starred': new_status})

# --- Lambda Handlers ---

# 1. API Handler (HTTP requests)
lambda_handler = make_lambda_handler(app)

# 2. Scheduled Handler (EventBridge/Cron)
def scheduled_update_handler(event, context):
    print("Starting scheduled price update...")
    count = db.update_prices()
    print(f"Updated {count} stocks.")
    return {'statusCode': 200, 'body': f'Updated {count} stocks'}

if __name__ == '__main__':
    # Local development only
    # Note: This will fail without AWS credentials configured locally if it tries to hit DynamoDB
    # You might want to mock db.py for pure local testing without AWS
    app.run(debug=True, port=5000)
