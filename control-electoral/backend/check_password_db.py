from sqlalchemy import create_engine, text
import os

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://elector:passwd@db:5432/elector_db')
engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    result = conn.execute(text("SELECT cedula, password, LENGTH(password) as pwd_len FROM delegados WHERE cedula = 'delegado1@example.com'"))
    row = result.fetchone()
    if row:
        cedula, pwd, pwd_len = row
        print(f"Cedula: {cedula}")
        print(f"Password length: {pwd_len}")
        print(f"Password stored: {pwd[:80] if pwd else 'NULL'}...")
        
        # Verificar si el hash es válido
        import bcrypt
        if pwd:
            try:
                # Si pwd_len < 60, probablemente no es un hash válido
                if pwd_len < 60:
                    print(f"⚠️  Password hash demasiado corto ({pwd_len} chars, debería ser ~60)")
                
                # Intentar verificar
                result = bcrypt.checkpw(b'delegado123', pwd.encode() if isinstance(pwd, str) else pwd)
                print(f"Verification result: {result}")
            except Exception as e:
                print(f"Error during verification: {type(e).__name__}: {e}")
    else:
        print("No se encontró el delegado")
