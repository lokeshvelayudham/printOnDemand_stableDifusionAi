import requests
import pandas as pd
import base64
import os

# Set your API credentials 
access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzN2Q0YmQzMDM1ZmUxMWU5YTgwM2FiN2VlYjNjY2M5NyIsImp0aSI6ImQwN2M5ZDUxNjBmZWFhMmRiZTg4NzliNTlmMjA3ZDYwYmQ3MTliOTA5MTZlMDQ1MjJlYWEwYmY4NzI4MmRhYTJkYTRlMzY2ZGUzNzQwOTUwIiwiaWF0IjoxNjkwODE4MDkxLjkwNTIxOCwibmJmIjoxNjkwODE4MDkxLjkwNTIyLCJleHAiOjE3MjI0NDA0OTEuODk5MjI3LCJzdWIiOiIxNDU3Nzc0NCIsInNjb3BlcyI6WyJzaG9wcy5tYW5hZ2UiLCJzaG9wcy5yZWFkIiwiY2F0YWxvZy5yZWFkIiwib3JkZXJzLnJlYWQiLCJvcmRlcnMud3JpdGUiLCJwcm9kdWN0cy5yZWFkIiwicHJvZHVjdHMud3JpdGUiLCJ3ZWJob29rcy5yZWFkIiwid2ViaG9va3Mud3JpdGUiLCJ1cGxvYWRzLnJlYWQiLCJ1cGxvYWRzLndyaXRlIiwicHJpbnRfcHJvdmlkZXJzLnJlYWQiXX0.ATGgcSR-IUGdj6qbx0XztGpuKJ-cFUc5y2w4A7bug9NUMcrIphmoOIU9yjLp4JR5IZ_G94E8HKQUtcDqH-k"

# Find your shop ID by running this: curl -X GET https://api.printify.com/v1/shops.json --header "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzN2Q0YmQzMDM1ZmUxMWU5YTgwM2FiN2VlYjNjY2M5NyIsImp0aSI6ImQwN2M5ZDUxNjBmZWFhMmRiZTg4NzliNTlmMjA3ZDYwYmQ3MTliOTA5MTZlMDQ1MjJlYWEwYmY4NzI4MmRhYTJkYTRlMzY2ZGUzNzQwOTUwIiwiaWF0IjoxNjkwODE4MDkxLjkwNTIxOCwibmJmIjoxNjkwODE4MDkxLjkwNTIyLCJleHAiOjE3MjI0NDA0OTEuODk5MjI3LCJzdWIiOiIxNDU3Nzc0NCIsInNjb3BlcyI6WyJzaG9wcy5tYW5hZ2UiLCJzaG9wcy5yZWFkIiwiY2F0YWxvZy5yZWFkIiwib3JkZXJzLnJlYWQiLCJvcmRlcnMud3JpdGUiLCJwcm9kdWN0cy5yZWFkIiwicHJvZHVjdHMud3JpdGUiLCJ3ZWJob29rcy5yZWFkIiwid2ViaG9va3Mud3JpdGUiLCJ1cGxvYWRzLnJlYWQiLCJ1cGxvYWRzLndyaXRlIiwicHJpbnRfcHJvdmlkZXJzLnJlYWQiXX0.ATGgcSR-IUGdj6qbx0XztGpuKJ-cFUc5y2w4A7bug9NUMcrIphmoOIU9yjLp4JR5IZ_G94E8HKQUtcDqH-k"

shop_id = "10877841"

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

    # To change the print object, use this to find the variant id curl -X GET "https://api.printify.com/v1/catalog/blueprints/1098/print_providers/228/variants.json" "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzN2Q0YmQzMDM1ZmUxMWU5YTgwM2FiN2VlYjNjY2M5NyIsImp0aSI6ImQwN2M5ZDUxNjBmZWFhMmRiZTg4NzliNTlmMjA3ZDYwYmQ3MTliOTA5MTZlMDQ1MjJlYWEwYmY4NzI4MmRhYTJkYTRlMzY2ZGUzNzQwOTUwIiwiaWF0IjoxNjkwODE4MDkxLjkwNTIxOCwibmJmIjoxNjkwODE4MDkxLjkwNTIyLCJleHAiOjE3MjI0NDA0OTEuODk5MjI3LCJzdWIiOiIxNDU3Nzc0NCIsInNjb3BlcyI6WyJzaG9wcy5tYW5hZ2UiLCJzaG9wcy5yZWFkIiwiY2F0YWxvZy5yZWFkIiwib3JkZXJzLnJlYWQiLCJvcmRlcnMud3JpdGUiLCJwcm9kdWN0cy5yZWFkIiwicHJvZHVjdHMud3JpdGUiLCJ3ZWJob29rcy5yZWFkIiwid2ViaG9va3Mud3JpdGUiLCJ1cGxvYWRzLnJlYWQiLCJ1cGxvYWRzLndyaXRlIiwicHJpbnRfcHJvdmlkZXJzLnJlYWQiXX0.ATGgcSR-IUGdj6qbx0XztGpuKJ-cFUc5y2w4A7bug9NUMcrIphmoOIU9yjLp4JR5IZ_G94E8HKQUtcDqH-k"
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
            }
        ],
        "print_areas": [
            {
                "variant_ids": [82064],  # Replace with the actual variant ID
                "placeholders": [
                    {
                        "position": "front",
                        "height": 3761,
                        "width": 3319,
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
