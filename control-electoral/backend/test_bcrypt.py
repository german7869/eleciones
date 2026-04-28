import bcrypt

# Test directo de hash y verificación
password = 'delegado123'

# Crear un hash como lo hace hash_password()
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12)).decode()
print(f"Hash generado: {hashed[:50]}...")

# Verificar como lo hace verify_password()
is_valid = bcrypt.checkpw(password.encode(), hashed.encode())
print(f"Verificación: {is_valid}")

# Intentar de otra forma
try:
    is_valid2 = bcrypt.checkpw(password.encode(), hashed.encode())
    print(f"Verificación 2: {is_valid2}")
except Exception as e:
    print(f"Error: {e}")
