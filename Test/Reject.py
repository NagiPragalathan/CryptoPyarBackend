import requests
import json

# Define the base URL of the API
BASE_URL = "http://127.0.0.1:8000/api/rejectd/"

# Create a new Rejectd entry
def create_rejectd(from_address, rejected_address):
    url = BASE_URL
    payload = {
        "from_address": from_address,
        "rejected_address": rejected_address
    }
    response = requests.post(url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
    print(f"Create Status Code: {response.status_code}")
    print(f"Create Response Content: {response.text}")
    return response.json()

# Retrieve all Rejectd entries
def get_all_rejectd():
    url = f"{BASE_URL}all/"
    response = requests.get(url)
    print(f"Get All Status Code: {response.status_code}")
    print(f"Get All Response Content: {response.text}")
    return response.json()

# Retrieve a single Rejectd entry by UUID
def get_rejectd(uuid):
    url = f"{BASE_URL}{uuid}/"
    response = requests.get(url)
    print(f"Get Single Status Code: {response.status_code}")
    print(f"Get Single Response Content: {response.text}")
    return response.json()

# Update a Rejectd entry by UUID
def update_rejectd(uuid, from_address, rejected_address):
    url = f"{BASE_URL}{uuid}/update/"
    payload = {
        "from_address": from_address,
        "rejected_address": rejected_address
    }
    response = requests.put(url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
    print(f"Update Status Code: {response.status_code}")
    print(f"Update Response Content: {response.text}")
    return response.json()

# Delete a Rejectd entry by UUID
def delete_rejectd(uuid):
    url = f"{BASE_URL}{uuid}/delete/"
    response = requests.delete(url)
    print(f"Delete Status Code: {response.status_code}")
    print(f"Delete Response Content: {response.text}")
    return response.status_code

# Test the API
if __name__ == "__main__":
    # Create a new Rejectd entry
    new_entry = create_rejectd("example@domain.com", "rejected@domain.com")
    print("Created:", new_entry)

    # Get all Rejectd entries
    all_entries = get_all_rejectd()
    print("All Entries:", all_entries)

    # Get a single Rejectd entry by UUID
    uuid = new_entry['id']
    single_entry = get_rejectd(uuid)
    print("Single Entry:", single_entry)

    # Update the Rejectd entry
    updated_entry = update_rejectd(uuid, "example@domain.com", "new_rejected@domain.com")
    print("Updated:", updated_entry)

    # Delete the Rejectd entry
    delete_status = delete_rejectd(uuid)
    print("Deleted Status Code:", delete_status)
