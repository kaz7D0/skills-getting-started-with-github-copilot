"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
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


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    email = email.strip().lower()
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")

    # Get the specific activity
    activity = activities[activity_name]

    if email in activity["participants"]:
        raise HTTPException(status_code=409, detail="Student is already signed up for this activity")

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.post("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    email = email.strip().lower()
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")

    # Get the specific activity
    activity = activities[activity_name]

    if email not in activity["participants"]:
        raise HTTPException(status_code=404, detail="Student is not registered for this activity")

    # Remove student
    activity["participants"].remove(email)
    return {"message": f"Unregistered {email} from {activity_name}"}
