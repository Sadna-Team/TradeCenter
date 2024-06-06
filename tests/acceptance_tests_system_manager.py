import unittest
import pytest
from backend import create_app, clean_data

@pytest.fixture
def app():
    app = create_app()
    return app

@pytest.fixture
def clean():
    yield
    clean_data()

def test_cancel_membership_success(app, clean):
    pass
