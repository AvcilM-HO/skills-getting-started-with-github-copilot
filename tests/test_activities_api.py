def test_get_activities_returns_expected_structure(client):
    response = client.get("/activities")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, dict)
    assert data
    assert "Chess Club" in data

    activity = data["Chess Club"]
    for key in ["description", "schedule", "max_participants", "participants"]:
        assert key in activity
    assert isinstance(activity["participants"], list)


def test_signup_adds_participant(client):
    email = "new.student@mergington.edu"

    signup_response = client.post("/activities/Chess%20Club/signup", params={"email": email})

    assert signup_response.status_code == 200
    assert "message" in signup_response.json()

    activities_response = client.get("/activities")
    participants = activities_response.json()["Chess Club"]["participants"]
    assert email in participants


def test_signup_rejects_duplicate_participant(client):
    existing_email = "michael@mergington.edu"

    response = client.post("/activities/Chess%20Club/signup", params={"email": existing_email})

    assert response.status_code == 400
    assert "detail" in response.json()


def test_signup_rejects_unknown_activity(client):
    response = client.post("/activities/Unknown%20Club/signup", params={"email": "student@mergington.edu"})

    assert response.status_code == 404
    assert "detail" in response.json()


def test_unregister_removes_participant(client):
    email = "michael@mergington.edu"

    unregister_response = client.delete("/activities/Chess%20Club/participants", params={"email": email})

    assert unregister_response.status_code == 200
    assert "message" in unregister_response.json()

    activities_response = client.get("/activities")
    participants = activities_response.json()["Chess Club"]["participants"]
    assert email not in participants


def test_unregister_rejects_unknown_activity(client):
    response = client.delete("/activities/Unknown%20Club/participants", params={"email": "student@mergington.edu"})

    assert response.status_code == 404
    assert "detail" in response.json()


def test_unregister_rejects_non_member(client):
    response = client.delete(
        "/activities/Chess%20Club/participants",
        params={"email": "not.signed.up@mergington.edu"},
    )

    assert response.status_code == 404
    assert "detail" in response.json()
