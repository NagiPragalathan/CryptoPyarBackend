import requests
import json

# Define the base URL of the API
BASE_URL = "http://127.0.0.1:8000/api/favorites/"

# Create a new Favorite entry
def create_favorite(from_address, to_address):
    payload = {
        "from_address": from_address,
        "to_address": to_address,
        "accept_status": False  # Assuming default value
    }
    response = requests.post(BASE_URL, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
    print(f"Create Status Code: {response.status_code}")
    print(f"Create Response Content: {response.text}")
    return response.json()

# Retrieve all Favorite entries
def get_all_favorites():
    url = f"{BASE_URL}all/"
    response = requests.get(url)
    print(f"Get All Status Code: {response.status_code}")
    print(f"Get All Response Content: {response.text}")
    return response.json()

# Retrieve a single Favorite entry by to_address
def get_favorite(to_address):
    url = f"{BASE_URL}{to_address}/"
    response = requests.get(url)
    print(f"Get Single Status Code: {response.status_code}")
    print(f"Get Single Response Content: {response.text}")
    return response.json()

# Update a Favorite entry by to_address
def update_favorite(to_address, from_address, new_accept_status):
    url = f"{BASE_URL}{to_address}/update/"
    payload = {
        "from_address": from_address,
        "to_address": to_address,
        "accept_status": new_accept_status
    }
    response = requests.put(url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
    print(f"Update Status Code: {response.status_code}")
    print(f"Update Response Content: {response.text}")
    return response.json()

# Delete a Favorite entry by to_address
def delete_favorite(to_address):
    url = f"{BASE_URL}{to_address}/delete/"
    response = requests.delete(url)
    print(f"Delete Status Code: {response.status_code}")
    print(f"Delete Response Content: {response.text}")
    return response.status_code

# Test the API
if __name__ == "__main__":
    # Create a new Favorite entry
    new_entry = create_favorite("example@domain.com", "favorite@domain.com")
    print("Created:", new_entry)

    # Get all Favorite entries
    all_entries = get_all_favorites()
    print("All Entries:", all_entries)

    # Get a single Favorite entry by to_address
    to_address = new_entry['to_address']
    single_entry = get_favorite(to_address)
    print("Single Entry:", single_entry)

    # Update the Favorite entry
    updated_entry = update_favorite(to_address, "example@domain.com", True)
    print("Updated:", updated_entry)

    # Delete the Favorite entry
    delete_status = delete_favorite(to_address)
    print("Deleted Status Code:", delete_status)
