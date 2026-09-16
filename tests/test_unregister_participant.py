import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from fastapi.testclient import TestClient

from app import activities, app


def test_unregister_participant_success():
    client = TestClient(app)
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    activities[activity_name]["participants"].append(email)

    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in activities[activity_name]["participants"]


def test_unregister_participant_missing_student_returns_404():
    client = TestClient(app)
    activity_name = "Basketball Team"
    email = "ghost@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    assert response.status_code == 404
