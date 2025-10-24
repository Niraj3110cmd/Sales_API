from flask import Flask, jsonify
from datetime import datetime, timedelta
import random

app = Flask(__name__)

def generate_sales_data():
    """Generate random sales data for entire year 2024"""
    products = ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones', 'Webcam', 'USB Cable', 'Phone', 'Tablet', 'Charger', 'SSD', 'RAM']
    regions = ['North', 'South', 'East', 'West', 'Central']
    salespersons = ['John Smith', 'Sarah Johnson', 'Mike Brown', 'Emily Davis', 'Chris Wilson', 'Anna Lee', 'David Miller']
    
    sales_data = []
    
    # Fixed dates: January 1, 2024 to December 31, 2024
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31)
    
    # Calculate total days in 2024 (366 days - leap year)
    total_days = (end_date - start_date).days + 1
    
    # Generate 3-5 sales per day for entire year
    current_date = start_date
    while current_date <= end_date:
        num_sales_today = random.randint(3, 5)
        
        for _ in range(num_sales_today):
            product = random.choice(products)
            quantity = random.randint(1, 10)
            price = round(random.uniform(10, 1000), 2)
            
            sale = {
                'date': current_date.strftime('%Y-%m-%d'),
                'product': product,
                'region': random.choice(regions),
                'quantity': quantity,
                'price': price,
                'total': round(quantity * price, 2),
                'customer_id': f'CUST{random.randint(1000, 9999)}',
                'salesperson': random.choice(salespersons)
            }
            sales_data.append(sale)
        
        current_date += timedelta(days=1)
    
    return sales_data

@app.route('/')
def home():
    return jsonify({
        'message': 'Sales API is running!',
        'data_period': '2024-01-01 to 2024-12-31',
        'endpoints': {
            'all_sales': '/api/sales',
            'summary': '/api/sales/summary',
            'monthly': '/api/sales/monthly'
        }
    })

@app.route('/api/sales')
def get_sales():
    """Return all sales data for 2024"""
    return jsonify(generate_sales_data())

@app.route('/api/sales/summary')
def get_summary():
    """Return sales summary statistics for 2024"""
    sales_data = generate_sales_data()
    
    total_sales = sum(sale['total'] for sale in sales_data)
    total_quantity = sum(sale['quantity'] for sale in sales_data)
    avg_sale = total_sales / len(sales_data) if sales_data else 0
    
    summary = {
        'total_records': len(sales_data),
        'total_sales_value': round(total_sales, 2),
        'total_quantity_sold': total_quantity,
        'average_sale_value': round(avg_sale, 2),
        'date_range': {
            'start': '2024-01-01',
            'end': '2024-12-31'
        }
    }
    
    return jsonify(summary)

@app.route('/api/sales/monthly')
def get_monthly():
    """Return monthly aggregated sales data"""
    sales_data = generate_sales_data()
    
    # Aggregate by month
    monthly_data = {}
    for sale in sales_data:
        month = sale['date'][:7]  # Extract YYYY-MM
        if month not in monthly_data:
            monthly_data[month] = {
                'month': month,
                'total_sales': 0,
                'total_quantity': 0,
                'record_count': 0
            }
        monthly_data[month]['total_sales'] += sale['total']
        monthly_data[month]['total_quantity'] += sale['quantity']
        monthly_data[month]['record_count'] += 1
    
    # Convert to list and round values
    result = []
    for month in sorted(monthly_data.keys()):
        data = monthly_data[month]
        result.append({
            'month': month,
            'total_sales': round(data['total_sales'], 2),
            'total_quantity': data['total_quantity'],
            'record_count': data['record_count'],
            'average_sale': round(data['total_sales'] / data['record_count'], 2)
        })
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
