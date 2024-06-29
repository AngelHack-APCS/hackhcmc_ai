import requests

# Define the endpoint URL
url = 'http://localhost:8001/suggest'


# Send the GET request
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Print the response content
    print('Suggestions:', response.json())
else:
    print('Failed to retrieve suggestions:', response.status_code)
