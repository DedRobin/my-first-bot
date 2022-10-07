import pytest
from unittest import mock
from server import create_app


@pytest.mark.parametrize("method", ["get", "put", "patch", "delete"])
async def test_api(aiohttp_client, method):
    client = await aiohttp_client(create_app())
    response = await getattr(client, method)("/")
    assert response.status == 405


@mock.patch("server.send_message")
async def test_api_validation(send_message_mock, aiohttp_client):
    client = await aiohttp_client(create_app())

    response = await client.post("/", data={})
    assert response.status == 415

    response = await client.post("/", json={"test": "test"})
    assert response.status == 400

    response = await client.post("/", json={"message": ""})
    assert response.status == 200
    assert send_message_mock.called

    response = await client.post("/", json={"message": "message"})
    assert response.status == 200
    assert send_message_mock.called
