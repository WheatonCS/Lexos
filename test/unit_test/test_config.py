import pytest
from lexos.application import app


@pytest.fixture
def client():
    return app.test_client()


def test_upload(client):
    rv = client.get("/statistics")
    temp = rv.data

    print("DONE")
