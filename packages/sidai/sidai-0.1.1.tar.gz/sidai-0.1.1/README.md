# The SID python package

This package provides a straight-forward wrapper around the [SID API](https://docs.sid.ai).
It uses `httpx` for handling http requests.

## Making a query
```python
token = '<TOKEN>' # retrieve from database
res = sid.query(token=token, query="What does SID.ai do?")
for snippet in res.results:
    print(snippet)
```
Check out the [docs](https://docs.sid.ai) to learn how to get started with SID.
