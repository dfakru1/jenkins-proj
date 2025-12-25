FROM python:latest
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY backend backend
CMD ["uvicorn","backend.main:app"]