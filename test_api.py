import requests
import json

# Test the API with a simple order
test_data = {
    "order_id": "TEST-123",
    "customer_name": "Test User",
    "items": [
        {
            "product_id": 1,
            "name": "Test Product",
            "brand": "Test Brand",
            "price": 999,
            "quantity": 1
        }
    ],
    "total": 999,
    "address": "123 Test St, Test City, Test State - 123456",
    "payment_method": "Cash on Delivery"
}

try:
    response = requests.post(
        'http://localhost:5000/api/place_order',
        json=test_data,
        headers={'Content-Type': 'application/json'}
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
