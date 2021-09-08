FROM python:3.9-alpine
WORKDIR /app
COPY . ./
CMD ["python3", "./mitodo.py"]