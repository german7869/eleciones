import requests

r = requests.get('http://localhost:8000/ejemplos/parroquias_ejemplo.csv')
print(f'Status: {r.status_code}')
print(f'Content-Type: {r.headers.get("Content-Type")}')
print(f'Content-Disposition: {r.headers.get("Content-Disposition")}')
print(f'Body length: {len(r.content)}')
print('Body:', r.text)
