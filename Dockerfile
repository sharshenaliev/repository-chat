FROM python:3.10.6
WORKDIR /fastapi_app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000