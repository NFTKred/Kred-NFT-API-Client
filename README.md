# Python API

Simple Python client library to manage access to the Coin.Kred NFT API.

See http://docs.coin.kred for a full description of the API.

Usage example for the client library:
```python
from pprint import pprint
import cryptokred

ck = cryptokred.API(DEV_KEY)
pprint(ck.request('coins', data={'token': USER_TOKEN}))
```
