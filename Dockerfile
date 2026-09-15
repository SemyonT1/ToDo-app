FROM python:3.14-slim

RUN apt-get update && apt-get install -y curl

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 5000

CMD ["python3", "src/backend/app.py"]




