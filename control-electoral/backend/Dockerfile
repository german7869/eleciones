FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Generar archivos de ejemplo CSV
RUN python generate_csv_examples.py

# Hacer ejecutable el entrypoint
RUN chmod +x entrypoint.sh

CMD ["./entrypoint.sh"]
