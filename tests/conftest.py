import sys
import os
import pytest

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app  # Now this will work

@pytest.fixture
def client():
    from fastapi.testclient import TestClient
    with TestClient(app) as c:
        yield c

# .\venv\Scripts\activate   
# pytest tests/unit/
# pytest tests/integration/