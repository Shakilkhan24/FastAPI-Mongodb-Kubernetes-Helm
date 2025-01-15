FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

ENV MONGODB_URL="mongodb://mongodb:27017"

CMD ["uvicorn", "fastmongo:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
