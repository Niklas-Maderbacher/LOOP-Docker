from app.api.schemas.issue import StoryPointUpdate
from fastapi.testclient import TestClient
from app.main import app  # Import the FastAPI application

client = TestClient(app)

def test_update_issue_story_points_success():
    """
    Test case for successfully updating story points of an issue.

    Steps:
    1. A valid issue ID and new story point value (5) are provided.
    2. The `PATCH` request is sent to the `/api/v1/issues/{issue_id}` endpoint with the new story point value.
    3. The response status code is checked to be 200 OK.
    4. The updated issue is returned, and its `story_points` field is checked to ensure it has been updated to the new value (5).
    
    Expected outcome:
    - The response status code should be 200.
    - The `story_points` field should be equal to the provided value (5).
    """
    issue_id = 1
    update_data = StoryPointUpdate(new_story_point_value=5)
    
    response = client.patch(f"/api/v1/issues/{issue_id}", json=update_data.dict())
    
    assert response.status_code == 200
    updated_issue = response.json()
    assert updated_issue["story_points"] == 5  # Check if story points were updated correctly

def test_update_issue_story_points_failure_negative_value():
    """
    Test case for failing to update story points with a negative value.

    Steps:
    1. A valid issue ID and an invalid story point value (-1) are provided.
    2. The `PATCH` request is sent to the `/api/v1/issues/{issue_id}` endpoint with the negative story point value.
    3. The response status code is checked to be 400 Bad Request.
    4. The error message returned is checked to ensure it matches the expected message that story points must be positive integers.

    Expected outcome:
    - The response status code should be 400 (Bad Request).
    - The response JSON should contain the correct error message: "Story points need to be positive integer values."
    """
    issue_id = 1
    update_data = StoryPointUpdate(new_story_point_value=-1)
    
    response = client.patch(f"/api/v1/issues/{issue_id}", json=update_data.dict())
    
    assert response.status_code == 400
    assert response.json() == {"detail": "Story points need to be positive integer values."}  # Check if the error message is correct

def test_update_issue_story_points_no_update():
    """
    Test case for no update to story points when the new value is the same as the current one (0 in this case).

    Steps:
    1. A valid issue ID and a new story point value (0) are provided (assuming the current value is also 0).
    2. The `PATCH` request is sent to the `/api/v1/issues/{issue_id}` endpoint with the story point value of 0.
    3. The response status code is checked to be 200 OK, as no actual update is needed.
    
    Expected outcome:
    - The response status code should be 200 OK, indicating that the update was processed but no change was made.
    """
    issue_id = 1
    update_data = StoryPointUpdate(new_story_point_value=0)  # Assuming no change to story points
    response = client.patch(f"/api/v1/issues/{issue_id}", json=update_data.dict())

    assert response.status_code == 200  # Expecting 200 OK even though there was no update
