FROM python:3.12
WORKDIR /app
COPY src/requirements.txt /app/
COPY src /app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "csv_to_db.py"]