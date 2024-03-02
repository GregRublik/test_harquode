import requests

# response = requests.get('http://localhost:7000/products/')
# data = response.json()
response = requests.get('http://localhost:7000/lessons/1/')
data = response
print(data)
