import boto3
import os
import random
from decimal import Decimal

# Get table name from environment variable (set by SAM)
TABLE_NAME = os.environ.get('TABLE_NAME', 'StockTrackerTable')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

def get_all_stocks():
    """Scan the table to get all stocks."""
    try:
        response = table.scan()
        items = response.get('Items', [])
        # Convert Decimal to float for JSON serialization
        for item in items:
            item['price'] = float(item['price'])
            item['change'] = float(item['change'])
        return items
    except Exception as e:
        print(f"Error fetching stocks: {e}")
        return []

def add_stock(symbol):
    """Add a new stock with a random initial price."""
    symbol = symbol.upper()
    # Check if exists
    existing = table.get_item(Key={'symbol': symbol})
    if 'Item' in existing:
        return None, "Stock already exists"

    new_stock = {
        'symbol': symbol,
        'price': Decimal(str(round(random.uniform(10, 1000), 2))),
        'starred': False,
        'change': Decimal('0.0')
    }
    
    try:
        table.put_item(Item=new_stock)
        # Convert back to float for response
        new_stock['price'] = float(new_stock['price'])
        new_stock['change'] = float(new_stock['change'])
        return new_stock, None
    except Exception as e:
        return None, str(e)

def toggle_star(symbol):
    """Toggle the starred status of a stock."""
    symbol = symbol.upper()
    try:
        # First get current status
        response = table.get_item(Key={'symbol': symbol})
        if 'Item' not in response:
            return None, "Stock not found"
        
        current_status = response['Item'].get('starred', False)
        new_status = not current_status
        
        table.update_item(
            Key={'symbol': symbol},
            UpdateExpression="set starred = :s",
            ExpressionAttributeValues={':s': new_status},
            ReturnValues="UPDATED_NEW"
        )
        return new_status, None
    except Exception as e:
        return None, str(e)

def update_prices():
    """Update prices for all stocks (for scheduled task)."""
    stocks = get_all_stocks()
    updated_count = 0
    
    for stock in stocks:
        symbol = stock['symbol']
        current_price = stock['price']
        
        # Simulate price change
        change_percent = random.uniform(-0.02, 0.02)
        new_price = current_price * (1 + change_percent)
        
        # Update in DB
        try:
            table.update_item(
                Key={'symbol': symbol},
                UpdateExpression="set price = :p, change = :c",
                ExpressionAttributeValues={
                    ':p': Decimal(str(round(new_price, 2))),
                    ':c': Decimal(str(round(change_percent * 100, 2)))
                }
            )
            updated_count += 1
        except Exception as e:
            print(f"Failed to update {symbol}: {e}")
            
    return updated_count
