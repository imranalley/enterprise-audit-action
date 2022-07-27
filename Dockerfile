FROM python:3-slim
WORKDIR /app
COPY . /app
RUN pip install --target=/app -r requirements.txt
CMD ["python", "/app/main.py"]