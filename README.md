# CryptoKred

Simple python client library to manage access to the Kred NFT API

See http://docs.crypto.kred for a full description of the API.

Usage example for the client library:
```python
from pprint import pprint
import cryptokred

ck = cryptokred.API(DEV_KEY)
pprint(ck.request('coins', data={'token': USER_TOKEN}))
```
