# /
## GET
Api Docs

# /sign
## POST
- Content: HASH
- Credentials

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