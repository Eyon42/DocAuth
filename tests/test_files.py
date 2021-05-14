# pylint: disable=redefined-outer-name

import hashlib


def test_file_update(client, sample_user):
    file_hash = hashlib.sha256("I'm not a bad file".encode()).hexdigest()
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

def test_sign_file(client, sample_user, sample_contract, sample_file):
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
    file_hash = hashlib.sha256("not a real file".encode()).hexdigest()
    rv = client.put(f"api/files/{file_hash}/signature", query_string={
            "token" : sample_user["token"]
        })
    
    assert rv.status_code == 404

# TODO:
# Test with real files
# Test file modifications
