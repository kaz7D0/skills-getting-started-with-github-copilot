"""
Unit tests for FastAPI application endpoints.

Tests cover all main endpoints:
- GET / (root/redirect)
- GET /activities (get all activities)
- POST /activities/{activity_name}/signup (sign up for activity)
- POST /activities/{activity_name}/unregister (unregister from activity)
"""

import pytest


class TestRootEndpoint:
    """Tests for the GET / endpoint."""
    
    def test_root_redirects_to_static_index(self, client):
        """Test that GET / returns a redirect to /static/index.html"""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"


class TestGetActivitiesEndpoint:
    """Tests for the GET /activities endpoint."""
    
    def test_get_activities_returns_all_activities(self, client):
        """Test that GET /activities returns all activities"""
        response = client.get("/activities")
        assert response.status_code == 200
        data = response.json()
        
        # Verify all 9 activities are present
        assert len(data) == 9
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Soccer Team",
            "Basketball Team",
            "Art Club",
            "Music Ensemble",
            "Debate Team",
            "Math Club"
        ]
        for activity_name in expected_activities:
            assert activity_name in data
    
    def test_get_activities_returns_activity_details(self, client):
        """Test that each activity has required fields"""
        response = client.get("/activities")
        data = response.json()
        
        # Check that each activity has required fields
        for activity_name, activity_details in data.items():
            assert "description" in activity_details
            assert "schedule" in activity_details
            assert "max_participants" in activity_details
            assert "participants" in activity_details
            assert isinstance(activity_details["participants"], list)


class TestSignupEndpoint:
    """Tests for the POST /activities/{activity_name}/signup endpoint."""
    
    def test_signup_success(self, client, existing_activity, sample_email):
        """Test successful signup for an activity"""
        response = client.post(
            f"/activities/{existing_activity}/signup",
            params={"email": sample_email}
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert sample_email in data["message"]
        assert existing_activity in data["message"]
    
    def test_signup_missing_email(self, client, existing_activity):
        """Test signup fails when email parameter is missing"""
        response = client.post(
            f"/activities/{existing_activity}/signup"
        )
        assert response.status_code == 422  # Unprocessable Entity
    
    def test_signup_empty_email(self, client, existing_activity):
        """Test signup fails when email is empty"""
        response = client.post(
            f"/activities/{existing_activity}/signup",
            params={"email": ""}
        )
        assert response.status_code == 400
        assert "Email is required" in response.json()["detail"]
    
    def test_signup_nonexistent_activity(self, client, sample_email, nonexistent_activity):
        """Test signup fails for non-existent activity"""
        response = client.post(
            f"/activities/{nonexistent_activity}/signup",
            params={"email": sample_email}
        )
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_signup_duplicate_student(self, client, existing_activity, sample_email):
        """Test signup fails when student is already signed up"""
        # Get the existing participants for the activity
        response = client.get("/activities")
        activity_data = response.json()[existing_activity]
        existing_participant = activity_data["participants"][0]
        
        # Try to sign up with an email already in participants
        response = client.post(
            f"/activities/{existing_activity}/signup",
            params={"email": existing_participant}
        )
        assert response.status_code == 409
        assert "already signed up" in response.json()["detail"]
    
    def test_signup_email_normalized(self, client, existing_activity):
        """Test that emails are normalized (stripped and lowercased)"""
        email_with_spaces = "  Test@Mergington.edu  "
        response = client.post(
            f"/activities/{existing_activity}/signup",
            params={"email": email_with_spaces}
        )
        assert response.status_code == 200
        
        # Verify by checking the activity
        response = client.get("/activities")
        participants = response.json()[existing_activity]["participants"]
        assert "test@mergington.edu" in participants


class TestUnregisterEndpoint:
    """Tests for the POST /activities/{activity_name}/unregister endpoint."""
    
    def test_unregister_success(self, client, existing_activity):
        """Test successful unregister from an activity"""
        # Get an existing participant
        response = client.get("/activities")
        activity_data = response.json()[existing_activity]
        existing_participant = activity_data["participants"][0]
        
        # Unregister the participant
        response = client.post(
            f"/activities/{existing_activity}/unregister",
            params={"email": existing_participant}
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert existing_participant in data["message"]
        assert existing_activity in data["message"]
    
    def test_unregister_missing_email(self, client, existing_activity):
        """Test unregister fails when email parameter is missing"""
        response = client.post(
            f"/activities/{existing_activity}/unregister"
        )
        assert response.status_code == 422  # Unprocessable Entity
    
    def test_unregister_empty_email(self, client, existing_activity):
        """Test unregister fails when email is empty"""
        response = client.post(
            f"/activities/{existing_activity}/unregister",
            params={"email": ""}
        )
        assert response.status_code == 400
        assert "Email is required" in response.json()["detail"]
    
    def test_unregister_nonexistent_activity(self, client, sample_email, nonexistent_activity):
        """Test unregister fails for non-existent activity"""
        response = client.post(
            f"/activities/{nonexistent_activity}/unregister",
            params={"email": sample_email}
        )
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_unregister_not_registered_student(self, client, existing_activity, sample_email):
        """Test unregister fails when student is not registered"""
        response = client.post(
            f"/activities/{existing_activity}/unregister",
            params={"email": sample_email}
        )
        assert response.status_code == 404
        assert "not registered" in response.json()["detail"]
    
    def test_unregister_email_normalized(self, client, existing_activity):
        """Test that emails are normalized (stripped and lowercased) during unregister"""
        # Get an existing participant
        response = client.get("/activities")
        activity_data = response.json()[existing_activity]
        existing_participant = activity_data["participants"][0]
        
        # Unregister with email that has spaces and mixed case
        email_with_variations = f"  {existing_participant.upper()}  "
        response = client.post(
            f"/activities/{existing_activity}/unregister",
            params={"email": email_with_variations}
        )
        assert response.status_code == 200


class TestSignupAndUnregisterFlow:
    """Integration tests for signup and unregister flow."""
    
    def test_signup_then_unregister(self, client, existing_activity, sample_email):
        """Test complete flow: signup -> verify -> unregister"""
        # Sign up
        response = client.post(
            f"/activities/{existing_activity}/signup",
            params={"email": sample_email}
        )
        assert response.status_code == 200
        
        # Verify signup worked
        response = client.get("/activities")
        participants = response.json()[existing_activity]["participants"]
        assert sample_email in participants
        
        # Unregister
        response = client.post(
            f"/activities/{existing_activity}/unregister",
            params={"email": sample_email}
        )
        assert response.status_code == 200
        
        # Verify unregister worked
        response = client.get("/activities")
        participants = response.json()[existing_activity]["participants"]
        assert sample_email not in participants
