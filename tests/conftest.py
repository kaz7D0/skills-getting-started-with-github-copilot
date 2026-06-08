"""
Test configuration and fixtures for FastAPI tests.

This module provides shared fixtures and test data for all test modules.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


# Initial state of activities for resetting between tests
INITIAL_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Build teamwork and improve soccer skills through practice and matches",
        "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": ["noah@mergington.edu", "ava@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Train for basketball drills, scrimmages, and school games",
        "schedule": "Tuesdays and Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["liam@mergington.edu", "isabella@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore drawing, painting, and creative projects",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["chloe@mergington.edu", "ethan@mergington.edu"]
    },
    "Music Ensemble": {
        "description": "Practice instruments and perform as a group",
        "schedule": "Mondays and Wednesdays, 3:30 PM - 4:45 PM",
        "max_participants": 14,
        "participants": ["mia@mergington.edu", "lucas@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop public speaking and argumentation skills through debates",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["harper@mergington.edu", "benjamin@mergington.edu"]
    },
    "Math Club": {
        "description": "Solve challenging problems and explore mathematical thinking",
        "schedule": "Fridays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["ella@mergington.edu", "henry@mergington.edu"]
    }
}


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Reset activities to their initial state before each test.
    
    This fixture is automatically used by all tests (autouse=True) to ensure
    a clean state for each test, preventing cross-test contamination.
    """
    # Reset the activities dictionary
    activities.clear()
    activities.update({
        name: {
            "description": data["description"],
            "schedule": data["schedule"],
            "max_participants": data["max_participants"],
            "participants": data["participants"].copy()  # Copy list to avoid mutation
        }
        for name, data in INITIAL_ACTIVITIES.items()
    })
    yield


@pytest.fixture
def client():
    """
    Provides a TestClient instance for testing the FastAPI application.
    
    Returns:
        TestClient: A test client for making requests to the FastAPI app.
    """
    return TestClient(app)


@pytest.fixture
def sample_email():
    """
    Provides a sample email address for testing.
    
    Returns:
        str: A valid email address for test signup/unregister operations.
    """
    return "test@mergington.edu"


@pytest.fixture
def existing_activity():
    """
    Provides the name of an existing activity in the database.
    
    Returns:
        str: An activity name that exists in the app.
    """
    return "Chess Club"


@pytest.fixture
def nonexistent_activity():
    """
    Provides the name of a non-existent activity.
    
    Returns:
        str: An activity name that does not exist in the app.
    """
    return "Nonexistent Activity"
