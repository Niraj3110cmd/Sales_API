from flask import Flask, jsonify
from datetime import datetime, timedelta
import random

app = Flask(__name__)

# Sample sales data generator
def generate_sales_data():
    products = ["Laptop", "Phone", "Tablet", "Monitor", "Keyboard", "Mouse", "Headphones"]
    regions = ["North", "South", "East", "West"]
    sales_data = []
    
    # Generate last 30 days of sales
    for i in range(30):
        date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        for _ in range(random.randint(5, 15)):  # Random number of sales per day
            sale = {
                "date": date,
                "product": random.choice(products),
                "region": random.choice(regions),
                "quantity": random.randint(1, 10),
                "unit_price": round(random.uniform(50, 1500), 2),
                "customer_id": f"CUST{random.randint(1000, 9999)}",
                "salesperson": f"SP{random.randint(1, 20)}"
            }
            sale["total_amount"] = round(sale["quantity"] * sale["unit_price"], 2)
            sales_data.append(sale)
    
    return sales_data

# API endpoint for sales data
@app.route('/')
def home():
    return """
    <h1>Sales Data API</h1>
    <p>Available endpoints:</p>
    <ul>
        <li><a href="/api/sales">/api/sales</a> - Get all sales data (JSON)</li>
        <li><a href="/api/sales/summary">/api/sales/summary</a> - Get sales summary</li>
    </ul>
    """

@app.route('/api/sales')
def get_sales():
    sales_data = generate_sales_data()
    return jsonify({
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "total_records": len(sales_data),
        "data": sales_data
    })

@app.route('/api/sales/summary')
def get_summary():
    sales_data = generate_sales_data()
    
    total_sales = sum(sale["total_amount"] for sale in sales_data)
    total_quantity = sum(sale["quantity"] for sale in sales_data)
    
    return jsonify({
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total_sales_amount": round(total_sales, 2),
            "total_quantity_sold": total_quantity,
            "total_transactions": len(sales_data),
            "average_transaction_value": round(total_sales / len(sales_data), 2)
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
