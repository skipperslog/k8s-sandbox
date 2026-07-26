FROM python:3.12-slim
WORKDIR /app
RUN pip install flask prometheus_flask_exporter
COPY app.py .
EXPOSE 8080
CMD ["python", "app.py"]
