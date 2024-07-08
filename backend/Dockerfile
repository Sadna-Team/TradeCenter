FROM python:3.12-slim

WORKDIR /app

# Copy requirements.txt
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the application
COPY . /app/

ENV PYTHONPATH=/app

CMD ["flask", "run", "--host=0.0.0.0"]
