# /
## GET
Api Docs

# /files
## POST
- Content:
  - Hash
  - filename
- Options
  - contract : bool
  - expire_date
- Return:
  - Created Document

# /files/{hash}|{id}?by_id=bool&
## GET
- Return:
  - Document

# /users/{id}
# GET

# /users/
# POST

# /verificate/{Hash}
## GET
- Response:

```
if Hash in db:
    {
        exists: True
        owner: file.owner_id
        date_added: file.date_added
    }
else:
    {
        exists: False
    }
```