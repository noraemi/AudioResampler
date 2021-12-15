import requests
import json

response = requests.get('')
for data in response.json()['items']:
    print(data['title'])
    print(data['link'])
    print()




