FROM python:3.9-slim

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY reverseproxy.py .
EXPOSE 5000

CMD ["python", "./reverseproxy.py"]
