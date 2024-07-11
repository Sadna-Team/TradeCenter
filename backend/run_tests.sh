#!/bin/bash

# Load environment variables from .env if running locally
if [ -z "$POSTGRES_USER" ]; then
  # Source environment variables
  if [ -f .env ]; then
    export $(cat .env | xargs)
  else
    echo ".env file not found."
    exit 1
  fi
fi

# Wait for the database to be ready
echo "Waiting for the database to be ready..."
until pg_isready -h db -p 5432 -U "${POSTGRES_USER}"; do
  sleep 1
done
echo "Database is ready."

# Run pytest for pytest-based tests
echo "Running pytest tests..."
pytest tests/unit_tests
pytest tests/acceptance_test_checkout.py
pytest tests/acceptance_tests_roles.py
pytest tests/acceptance_tests_system_manager.py
pytest tests/acceptance_tests_user.py
pytest tests/concurrency_test.py
pytest tests/integration_tests.py
pytest tests/notification_test.py
pytest tests/store_owner_actions_acceptance_test.py
pytest tests/store_owner_more_actions_acceptance_test.py


# Add more unittest test files as needed

echo "Tests completed."
