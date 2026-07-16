import os
import pytest 

@pytest.fixture(scope="session", autouse=True)
def setup_test_enviornment():
    """ 
    Sets up global environment variables for the entire test session before any application
    modules are imported.
    """
    os.environ["FRONTEND_REMOTE_URL"] = "https://www.example.com"
