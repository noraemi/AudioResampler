import requests

url = 'https://httpbin.org/post'

files = [
    ('copy1', ('cookies.csv', open('cookies.csv', 'rb'), 'csv')),
    ('copy2', ('cookies.csv', open('cookies.csv', 'rb'), 'csv'))
]

r = requests.post(url, files=files)
print(r.status_code)
print(r.text)
