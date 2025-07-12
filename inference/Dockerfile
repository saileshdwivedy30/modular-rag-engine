FROM python:3.10-slim

WORKDIR /app

COPY inference/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY inference/api_server.py .

CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000"]
