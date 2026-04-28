import requests

payload = {'cedula': 'delegado1@example.com', 'password': 'delegado123'}

try:
    response = requests.post('http://localhost:8000/auth/login', json=payload)
    data = response.json()
    print(f'Status: {response.status_code}')
    token = data.get("access_token")
    if token:
        print(f'Token: {token}')
        print(f'Rol: {data.get("rol")}')
    else:
        print(f'Error: {data}')
except Exception as e:
    print(f'Error: {e}')
