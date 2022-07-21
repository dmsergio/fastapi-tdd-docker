import json


def test_create_summary(test_app_with_db):
    # Given
    # test_app_with_db

    # When
    response = test_app_with_db.post(
        "/summaries/",
        data=json.dumps({"url": "https://foo.bar"}),
    )

    # Then
    assert response.status_code == 201
    assert response.json()["url"] == "https://foo.bar"


def test_create_summary_invalid_json(test_app_with_db):
    # Given
    # test_app_with_db

    # When
    response = test_app_with_db.post(
        "/summaries/",
        data=json.dumps({}),
    )

    # Then
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "url"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }


def test_read_summary(test_app_with_db):
    # Given
    response = test_app_with_db.post(
        "/summaries/",
        data=json.dumps({"url": "https://foo.bar"}),
    )
    summary_id = response.json()["id"]

    # When
    response = test_app_with_db.get(f"/summaries/{summary_id}/")

    # Then
    assert response.status_code == 200
    response_dict = response.json()
    assert response_dict["id"] == summary_id
    assert response_dict["url"] == "https://foo.bar"
    assert response_dict["summary"]
    assert response_dict["created_at"]


def test_read_summary_incorrect_id(test_app_with_db):
    # Given
    # test_app_with_db

    # When
    response = test_app_with_db.get("/summaries/999/")

    # Then
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"


def test_read_all_summaries(test_app_with_db):
    # Given
    response = test_app_with_db.post(
        "/summaries/",
        data=json.dumps({"url": "https://foo.bar"}),
    )
    summary_id = response.json()["id"]

    # When
    response = test_app_with_db.get("/summaries/")

    # Then
    response.status_code = 200
    res_list = response.json()
    assert len(list(filter(lambda x: x["id"] == summary_id, res_list))) == 1


def test_remove_summary(test_app_with_db):
    # Given
    response = test_app_with_db.post(
        "/summaries/",
        data=json.dumps({"url": "https://foo.bar"}),
    )
    summary_id = response.json()["id"]

    # When
    response = test_app_with_db.delete(f"/summaries/{summary_id}/")

    # Then
    assert response.status_code == 200
    assert response.json() == {
        "id": summary_id,
        "url": "https://foo.bar",
    }


def test_remove_summary_incorrect_id(test_app_with_db):
    # Given
    # no previous state

    # When
    response = test_app_with_db.delete("/summaries/999/")

    # Then
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"
