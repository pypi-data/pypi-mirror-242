# Kognic Query API Client

Python 3 library providing access to the Kognic Query API. 

To install with pip run `pip install kognic-query`

Set env KOGNIC_CREDENTIALS, see [kognic-auth](https://github.com/annotell/annotell-python/tree/master/kognic-auth). 

## Judgement Query Example
Stream all items matching a query
```python
from kognic.query.query_api_client import QueryApiClient
query_client = QueryApiClient()
resp = query_client.query_judgements(query_filter="requestId = X")
for item in resp.items():
    print(item)
```

## Change log

### 3.0.0
- Rebranded from Annotell to Kognic

### 2.5.0
- A new base Query client that can be inherrited for other applications 

### 2.4.1
- Use `annotell-auth[requests]>=2.0.0`

### 2.3.0
- Use `annotell-auth>=1.6`
- Remove metadata queries

### 2.2.0
- Use `annotell-auth>=1.5` with fault tolerant auth request session

### 2.1.0
- Use server default query limits 

### 2.0.0
- Rename library to `annotell-query`
- Rename `QueryApi` to `QueryApiClient`
- Add KPI query method

### 1.3.0
- Change constructor for authentication to only accept `auth`. 