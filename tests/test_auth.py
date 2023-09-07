from conftest import client


def test_register():
    response = client.post("/auth/register", json={
        "email": "string",
        "password": "string",
        "username": "string",
    })
    assert response.status_code == 201


def test_login():
    data = {
        "username": "string",
        "password": "string",
    }
    response = client.post("/auth/jwt/login", data=data)
    r = response.json()
    assert response.status_code == 200
    auth_token = r["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def test_logout():
    response = client.post("/auth/jwt/logout", headers=test_login())
    assert response.status_code == 204
