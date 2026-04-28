import requests
import json

# Prueba de login
login_url = 'http://localhost:8000/auth/login'
payload = {
    'cedula': 'delegado1@example.com',
    'password': 'delegado123'
}

print(f"Intentando login a {login_url}")
print(f"Payload: {json.dumps(payload)}")

try:
    response = requests.post(login_url, json=payload)
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nToken: {data.get('access_token')[:50]}...")
        print(f"Rol: {data.get('rol')}")
        print(f"✅ Login exitoso")
    else:
        print(f"❌ Error en login")
except Exception as e:
    print(f"Error: {e}")
