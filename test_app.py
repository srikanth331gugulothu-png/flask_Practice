import os

import pytest
from bson.objectid import ObjectId

from app import app, mongo


TEST_STUDENT_ID = ObjectId("66fddff25f4b5f6a0a123456")


@pytest.fixture
def client():
    """Create a Flask test client and prepare test data."""

    app.config["TESTING"] = True

    app.config["MONGO_URI"] = os.getenv(
        "MONGO_URI",
        "mongodb://localhost:27017/test_student_db"
    )

    client = app.test_client()

    with app.app_context():
        mongo.db.students.delete_many({})

        mongo.db.students.insert_one({
            "_id": TEST_STUDENT_ID,
            "name": "Test Student",
            "email": "test@student.com",
            "course": "Flask"
        })

    yield client

    with app.app_context():
        mongo.db.students.delete_many({})


def test_health_check(client):
    """Verify the application health endpoint."""

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json == {"status": "healthy"}


def test_home_page(client):
    """Verify the home page loads successfully."""

    response = client.get("/")

    assert response.status_code == 200
    assert b"Test Student" in response.data


def test_add_student(client):
    """Verify a new student can be added."""

    response = client.post(
        "/add",
        data={
            "name": "New User",
            "email": "newuser@student.com",
            "course": "Python"
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"New User" in response.data


def test_update_student(client):
    """Verify an existing student can be updated."""

    response = client.post(
        f"/update/{TEST_STUDENT_ID}",
        data={
            "name": "Updated Name",
            "email": "updated@student.com",
            "course": "DevOps"
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Updated Name" in response.data


def test_delete_student(client):
    """Verify an existing student can be deleted."""

    response = client.get(
        f"/delete/{TEST_STUDENT_ID}",
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Test Student" not in response.data