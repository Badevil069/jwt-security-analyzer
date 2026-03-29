FROM python:3.14-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create volume for reports
VOLUME ["/app/reports"]

# Set the entry point
ENTRYPOINT ["python", "main.py"]
CMD ["--help"]
