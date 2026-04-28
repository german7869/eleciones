FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Generar archivos de ejemplo CSV
RUN python generate_csv_examples.py

CMD python app/utils/init_db.py && uvicorn main:app --host 0.0.0.0 --port 8000
