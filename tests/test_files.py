# pylint: disable=redefined-outer-name


def test_file_upload(client, sample_user, file_hash):
    rv = client.post("api/files", json={
        "filename" : "test_file.txt",
        "file_hash" : file_hash,
        "is_contract" : True
        }, query_string={
            "token" : sample_user["token"]
        })
    assert b"file_hash" in rv.data

    # Test that file acessible
    rv = client.get(f"api/files/{file_hash}")

    assert b"filename" in rv.data


def test_upload_duplicate_file(client, sample_user, sample_file):
    rv = client.post("api/files", json={
        "filename" : "test_file.txt",
        "file_hash" : sample_file,
        "is_contract" : True
        }, query_string={
            "token" : sample_user["token"]
        })
    assert b"Hash already exists" in rv.data


def test_upload_invalid_file_hash(client, sample_user):
    # Too long
    # This case is handled by the schema validation, not the endpoint.
    rv = client.post("api/files", json={
        "filename" : "test_file.txt",
        "file_hash" : "24db7178bd4cfc95e47742c6a7784256315463432d0855bd58f3967dc3f74a61413b1305",
        "is_contract" : True
        }, query_string={
            "token" : sample_user["token"]
        })
    assert b"Longer than maximum length 64." in rv.data

    # Too short
    rv = client.post("api/files", json={
        "filename" : "test_file.txt",
        "file_hash" : "6f97e8cc43dea521c38026df518068057c70b8e77",
        "is_contract" : True
        }, query_string={
            "token" : sample_user["token"]
        })
    assert b"Invalid Hash" in rv.data

    # Not Hex, but correct lenght
    rv = client.post("api/files", json={
        "filename" : "test_file.txt",
        "file_hash" : "rZnLtnUjfRpROMVKjFvgXCcLMyiQXWokfPTvthjloqsBCcDyVcaMxriSBQiGzHjI",
        "is_contract" : True
        }, query_string={
            "token" : sample_user["token"]
        })
    assert b"Invalid Hash" in rv.data


def test_get_non_existent_file(client, file_hash):
    rv = client.get(f"api/files/{file_hash}")
    assert rv.status_code == 404


def test_sign_file(client, sample_user, sample_contract, sample_file, file_hash):
    # Sign contract
    rv = client.put(f"api/files/{sample_contract}/signature", query_string={
            "token" : sample_user["token"]
        })

    assert rv.status_code == 201

    # Sign non-contract
    rv = client.put(f"api/files/{sample_file}/signature", query_string={
            "token" : sample_user["token"]
        })

    assert rv.status_code == 400

    # Sign random string
    rv = client.put(f"api/files/{file_hash}/signature", query_string={
            "token" : sample_user["token"]
        })

    assert rv.status_code == 404
