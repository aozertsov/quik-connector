FROM python:3.9.7-slim-buster 

WORKDIR /app
COPY requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt
COPY . .

CMD ["python3", "connector.py"]
