import json

import pytest


def create_summary(app) -> int:
    response = app.post(
        "/summaries/",
        data=json.dumps(
            {"url": "https://foo.bar"},
        ),
    )
    assert response.status_code == 201
    response_dict = response.json()
    assert response_dict["url"] == "https://foo.bar"

    return response_dict["id"]


def test_create_summary(test_app_with_db):
    create_summary(test_app_with_db)


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


def test_create_summary_invalid_url(test_app_with_db):
    # Given
    # test_app_with_db

    # When
    response = test_app_with_db.post(
        "/summaries/",
        data=json.dumps({"url": "invalid://url"}),
    )

    # Then
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "URL scheme not permitted"


def test_read_summary(test_app_with_db):
    # Given
    summary_id = create_summary(test_app_with_db)

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


def test_read_summary_id_less_than_one(test_app_with_db):
    # Given
    # test_app_with_db

    # When
    response = test_app_with_db.get("/summaries/0/")

    # Then
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["path", "id"],
                "msg": "ensure this value is greater than 0",
                "type": "value_error.number.not_gt",
                "ctx": {"limit_value": 0},
            }
        ]
    }


def test_read_all_summaries(test_app_with_db):
    # Given
    summary_id = create_summary(test_app_with_db)

    # When
    response = test_app_with_db.get("/summaries/")

    # Then
    response.status_code = 200
    res_list = response.json()
    assert len(list(filter(lambda x: x["id"] == summary_id, res_list))) == 1


def test_remove_summary(test_app_with_db):
    # Given
    summary_id = create_summary(test_app_with_db)

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


def test_remove_summary_id_less_than_one(test_app_with_db):
    # Given
    # no previous state

    # When
    response = test_app_with_db.delete("/summaries/0/")

    # Then
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["path", "id"],
                "msg": "ensure this value is greater than 0",
                "type": "value_error.number.not_gt",
                "ctx": {"limit_value": 0},
            }
        ]
    }


def test_update_summary(test_app_with_db):
    # Given
    summary_id = create_summary(test_app_with_db)

    # When
    response = test_app_with_db.put(
        f"/summaries/{summary_id}/",
        data=json.dumps(
            {
                "url": "https://foo.bar",
                "summary": "Updated!",
            }
        ),
    )
    assert response.status_code == 200

    # Then
    response_dict = response.json()
    assert response_dict["id"] == summary_id
    assert response_dict["url"] == "https://foo.bar"
    assert response_dict["summary"] == "Updated!"
    assert response_dict["created_at"]


@pytest.mark.parametrize(
    "summary_id, payload, status_code, detail",
    [
        [
            999,
            {"url": "https://foo.bar", "summary": "updated!"},
            404,
            "Summary not found",
        ],
        [
            0,
            {"url": "https://foo.bar", "summary": "updated!"},
            422,
            [
                {
                    "loc": ["path", "id"],
                    "msg": "ensure this value is greater than 0",
                    "type": "value_error.number.not_gt",
                    "ctx": {"limit_value": 0},
                }
            ],
        ],
        [
            None,
            {},
            422,
            [
                {
                    "loc": ["body", "url"],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
                {
                    "loc": ["body", "summary"],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
            ],
        ],
        [
            None,
            {"url": "https://foo.bar"},
            422,
            [
                {
                    "loc": [
                        "body",
                        "summary",
                    ],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
            ],
        ],
    ],
)
def test_update_summary_invalid_data(
    test_app_with_db,
    summary_id,
    payload,
    status_code,
    detail,
):
    if summary_id is None:
        summary_id = create_summary(test_app_with_db)

    response = test_app_with_db.put(
        f"/summaries/{summary_id}/",
        data=json.dumps(payload),
    )

    assert response.status_code == status_code
    assert response.json()["detail"] == detail


def test_update_summary_incorrect_url(test_app_with_db):
    # Given
    summary_id = create_summary(test_app_with_db)

    # When
    response = test_app_with_db.put(
        f"/summaries/{summary_id}/",
        data=json.dumps({"url": "invalid://url", "summary": "updated!"}),
    )

    # Then
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "URL scheme not permitted"
