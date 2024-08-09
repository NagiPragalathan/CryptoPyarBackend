import requests

# Define the API endpoint URL
api_url = "https://vortex-server-three.vercel.app/api/entry-with-private"

# Data to be sent to the API
data = {
    "toaddress": "@123",
    "messagecontent": "hello",
    "timestamp": "09-08-2024",
    "privateKey": "0x8144e9a42fed8ff976703c0c2d24b410f86f004770a32876aed4172b303e020b"
}

# Send the POST request to the API
try:
    response = requests.post(api_url, json=data)
    response.raise_for_status()  # Raise an error for bad status codes

    # Print the response from the server
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
