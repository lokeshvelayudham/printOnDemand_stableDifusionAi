import requests
import pandas as pd
import base64
import os

# Set your API credentials 
access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzN2Q0YmQzMDM1ZmUxMWU5YTgwM2FiN2VlYjNjY2M5NyIsImp0aSI6IjMzM2Q1YWY5ODA3MWU1NWQ4MmMxMjY3MWQ3ZWMxOThjMzg5MGEwZDgwODY3ZWU5MDBkZjY1Y2E4NjcwNjAyMDQzYjUyZjkwZWY4MWVhMzAzIiwiaWF0IjoxNjkxMDcwMzE0LjQ0MjkyMSwibmJmIjoxNjkxMDcwMzE0LjQ0MjkyNiwiZXhwIjoxNzIyNjkyNzE0LjQzNDk1NSwic3ViIjoiMTQ1ODUyNDQiLCJzY29wZXMiOlsic2hvcHMubWFuYWdlIiwic2hvcHMucmVhZCIsImNhdGFsb2cucmVhZCIsIm9yZGVycy5yZWFkIiwib3JkZXJzLndyaXRlIiwicHJvZHVjdHMucmVhZCIsInByb2R1Y3RzLndyaXRlIiwid2ViaG9va3MucmVhZCIsIndlYmhvb2tzLndyaXRlIiwidXBsb2Fkcy5yZWFkIiwidXBsb2Fkcy53cml0ZSIsInByaW50X3Byb3ZpZGVycy5yZWFkIl19.AN-RA68Vcl4JJY4Y0cRhRT7phRrX9ldwZzeDR0HPx4YtA7nHjvMYuYjKC3KsoU4WKIRd9ptzrrTx9rV9TXc"

# Find your shop ID by running this: curl -X GET https://api.printify.com/v1/shops.json --header "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzN2Q0YmQzMDM1ZmUxMWU5YTgwM2FiN2VlYjNjY2M5NyIsImp0aSI6IjMzM2Q1YWY5ODA3MWU1NWQ4MmMxMjY3MWQ3ZWMxOThjMzg5MGEwZDgwODY3ZWU5MDBkZjY1Y2E4NjcwNjAyMDQzYjUyZjkwZWY4MWVhMzAzIiwiaWF0IjoxNjkxMDcwMzE0LjQ0MjkyMSwibmJmIjoxNjkxMDcwMzE0LjQ0MjkyNiwiZXhwIjoxNzIyNjkyNzE0LjQzNDk1NSwic3ViIjoiMTQ1ODUyNDQiLCJzY29wZXMiOlsic2hvcHMubWFuYWdlIiwic2hvcHMucmVhZCIsImNhdGFsb2cucmVhZCIsIm9yZGVycy5yZWFkIiwib3JkZXJzLndyaXRlIiwicHJvZHVjdHMucmVhZCIsInByb2R1Y3RzLndyaXRlIiwid2ViaG9va3MucmVhZCIsIndlYmhvb2tzLndyaXRlIiwidXBsb2Fkcy5yZWFkIiwidXBsb2Fkcy53cml0ZSIsInByaW50X3Byb3ZpZGVycy5yZWFkIl19.AN-RA68Vcl4JJY4Y0cRhRT7phRrX9ldwZzeDR0HPx4YtA7nHjvMYuYjKC3KsoU4WKIRd9ptzrrTx9rV9TXc"

shop_id = "10887629"

# Set the URL for the API endpoints
base_url = "https://api.printify.com/v1"
upload_url = f"{base_url}/uploads/images.json"
product_url = f"{base_url}/shops/{shop_id}/products.json"

# Load the CSV file
csv_path = "product_information.csv"  # Update this to your CSV file path
image_df = pd.read_csv(csv_path)

# Set headers for requests
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

for idx, row in image_df.iterrows():
    # Convert the image to Base64
    with open(row['local_path'], "rb") as img_file:
        img_b64 = base64.b64encode(img_file.read()).decode('utf-8')

    # Upload the image to the Printify media library
    data = {
        "file_name": row['file_name'],
        "contents": img_b64
    }
    response = requests.post(upload_url, headers=headers, json=data)
    image_id = response.json()["id"]

    # To change the print object, use this to find the variant id curl -X GET "https://api.printify.com/v1/catalog/blueprints/1098/print_providers/228/variants.json" "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzN2Q0YmQzMDM1ZmUxMWU5YTgwM2FiN2VlYjNjY2M5NyIsImp0aSI6IjMzM2Q1YWY5ODA3MWU1NWQ4MmMxMjY3MWQ3ZWMxOThjMzg5MGEwZDgwODY3ZWU5MDBkZjY1Y2E4NjcwNjAyMDQzYjUyZjkwZWY4MWVhMzAzIiwiaWF0IjoxNjkxMDcwMzE0LjQ0MjkyMSwibmJmIjoxNjkxMDcwMzE0LjQ0MjkyNiwiZXhwIjoxNzIyNjkyNzE0LjQzNDk1NSwic3ViIjoiMTQ1ODUyNDQiLCJzY29wZXMiOlsic2hvcHMubWFuYWdlIiwic2hvcHMucmVhZCIsImNhdGFsb2cucmVhZCIsIm9yZGVycy5yZWFkIiwib3JkZXJzLndyaXRlIiwicHJvZHVjdHMucmVhZCIsInByb2R1Y3RzLndyaXRlIiwid2ViaG9va3MucmVhZCIsIndlYmhvb2tzLndyaXRlIiwidXBsb2Fkcy5yZWFkIiwidXBsb2Fkcy53cml0ZSIsInByaW50X3Byb3ZpZGVycy5yZWFkIl19.AN-RA68Vcl4JJY4Y0cRhRT7phRrX9ldwZzeDR0HPx4YtA7nHjvMYuYjKC3KsoU4WKIRd9ptzrrTx9rV9TXc"
#    https://api.printify.com/v1/catalog/blueprints/6/print_providers/270/variants.json
   # Current settings are for wall art
   
    # Create the product with the uploaded image
    data = {
        "title": row['title'],
        "description": row['description'],
        "tags": row['tags'].split(', '),  # Assuming tags are comma-separated in the CSV
        "blueprint_id": 6,  # Replace with the actual blueprint ID
        "print_provider_id": 270,
        "variants": [
            {
                "id": 12126,  # Replace with the actual variant ID
                "price": 3999,
                "is_enabled": True
            },
            {
                "id": 12100,
                "price": 3999,
                "is_enabled": True
            }
        ],
        "print_areas": [
            {
                "variant_ids": [12126,12100],  # Replace with the actual variant ID
                "placeholders": [
                    {
                        "position": "front",
                        "height": 5100,
                        "width": 4500,
                        "images": [
                            {
                                "id": image_id,
                                "x": 0.5,
                                "y": 0.5,
                                "scale": 1.5,
                                "angle": 0
                            }
                        ]
                    }
                ]
            }
        ]
    }
    response = requests.post(product_url, headers=headers, json=data)
    if response.status_code >= 200 and response.status_code < 300:
        print(f"Product {idx+1} created successfully!")
    else:
        print(f"Failed to create product {idx+1}. Server responded with: {response.text}")
