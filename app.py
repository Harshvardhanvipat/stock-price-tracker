import threading
import time
import random
from flask import Flask, jsonify, request, render_template
from datetime import datetime

app = Flask(__name__)

# In-memory storage
# Structure: { 'AAPL': { 'price': 150.00, 'starred': False, 'history': [] } }
stocks = {
    'AAPL': {'price': 150.00, 'starred': False, 'change': 0.0},
    'GOOGL': {'price': 2800.00, 'starred': False, 'change': 0.0},
    'TSLA': {'price': 700.00, 'starred': True, 'change': 0.0},
    'AMZN': {'price': 3400.00, 'starred': False, 'change': 0.0},
    'MSFT': {'price': 299.00, 'starred': False, 'change': 0.0}
}

def update_prices():
    """Background task to update stock prices every 5 minutes (simulated)."""
    while True:
        print(f"[{datetime.now()}] Updating stock prices...")
        for symbol in stocks:
            # Simulate price change between -2% and +2%
            current_price = stocks[symbol]['price']
            change_percent = random.uniform(-0.02, 0.02)
            new_price = current_price * (1 + change_percent)
            
            stocks[symbol]['price'] = round(new_price, 2)
            stocks[symbol]['change'] = round(change_percent * 100, 2)
        
        print(f"[{datetime.now()}] Prices updated.")
        # Sleep for 5 minutes (300 seconds)
        # For demo purposes, let's make it 30 seconds so the user can see it working
        time.sleep(30) 

# Start background thread
tracker_thread = threading.Thread(target=update_prices, daemon=True)
tracker_thread.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stocks', methods=['GET'])
def get_stocks():
    # Convert dict to list for easier frontend consumption
    stock_list = []
    for symbol, data in stocks.items():
        stock_list.append({
            'symbol': symbol,
            'price': data['price'],
            'starred': data['starred'],
            'change': data['change']
        })
    return jsonify(stock_list)

@app.route('/api/stocks', methods=['POST'])
def add_stock():
    data = request.json
    symbol = data.get('symbol', '').upper()
    
    if not symbol:
        return jsonify({'error': 'Symbol is required'}), 400
    
    if symbol in stocks:
        return jsonify({'error': 'Stock already exists'}), 400
    
    # Initialize with a random price
    stocks[symbol] = {
        'price': round(random.uniform(10, 1000), 2),
        'starred': False,
        'change': 0.0
    }
    
    return jsonify({'message': f'Stock {symbol} added', 'stock': stocks[symbol]})

@app.route('/api/stocks/<symbol>/star', methods=['POST'])
def toggle_star(symbol):
    symbol = symbol.upper()
    if symbol not in stocks:
        return jsonify({'error': 'Stock not found'}), 404
    
    stocks[symbol]['starred'] = not stocks[symbol]['starred']
    return jsonify({'starred': stocks[symbol]['starred']})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
