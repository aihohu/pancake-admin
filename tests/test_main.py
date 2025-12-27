import pytest


@pytest.mark.asyncio
async def test_read_main(client):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "PancakeAdmin"}
