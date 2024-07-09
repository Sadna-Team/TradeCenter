FROM python:3.12-slim

WORKDIR /app

# Install necessary packages
RUN apt-get update && apt-get install -y postgresql-client

# Copy requirements.txt
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the application
COPY . /app/

# Copy the test script from the backend directory
COPY run_tests.sh /app/backend/

# Set the executable permission for the test script
RUN chmod +x /app/backend/run_tests.sh

ENV PYTHONPATH=/app

CMD ["flask", "run", "--host=0.0.0.0"]
