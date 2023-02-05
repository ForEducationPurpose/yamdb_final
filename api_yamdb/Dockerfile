FROM python:3.7-slim

# I guess we can drop  RUN mkdir app
WORKDIR /app

# We COPY from Dockerfile dir to /app since it is our's new workdirectory it is .
COPY . .

RUN pip3 install -r requirements.txt --no-cache-dir

CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000" ]