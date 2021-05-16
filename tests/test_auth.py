# pylint: disable=redefined-outer-name


def login(client, username, password):
    return client.post('api/login', json=dict(
        username=username,
        password=password))


def test_register(client):
    rv = client.post("api/register", json=dict(
        username="Test_user",
        password="password",
        name="Rimuru"))
    assert rv.status_code == 201


def test_register_duplicate(client):
    client.post("api/register", json=dict(
        username="Test_user",
        password="password",
        name="Rimuru"))

    rv = client.post("api/register", json=dict(
        username="Test_user",
        password="password",
        name="Rimuru"))
    assert b"Username already exists" in rv.data


def test_login(client, sample_user):
    rv = login(client, sample_user["username"], sample_user["password"])
    assert rv.status_code == 200

def test_login_no_credentials(client):
    rv =  client.post('api/login')
    assert b"Auth failed. No credentials provided" in rv.data

def test_login_wrong_password(client, sample_user):
    rv = login(client, sample_user["username"], sample_user["password"]+"!")
    assert b"Incorrect Password/Username" in rv.data

def test_login_wrong_username(client, sample_user):
    rv = login(client, sample_user["username"]+"!", sample_user["password"])
    assert b"Incorrect Password/Username" in rv.data


def test_auth_token(client, sample_user):
    # Access with token
    rv = client.get("api/test/auth", query_string={
            "token" : sample_user["token"]
        })
    assert b"you are logged in" in rv.data

    # Access without token
    rv = client.get("api/test/auth")

    assert rv.status_code == 403
