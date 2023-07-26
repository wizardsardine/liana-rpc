# liana-rpc
lianad JSON-RPC Python client.

Serves as a client to connect to a [lianad](https://github.com/wizardsardine/liana) running instance trough the RPC socket.

You can have a look to the [RPC API reference](https://github.com/wizardsardine/liana/blob/master/doc/API.md)

## Install

### From pip
```shell
pip install liana-rpc
```

### From Github repo:
```shell
pip install git+https://github.com/pythcoiner/liana-rpc
```

## Examples

### Connect
You might have a `lianad` running instance on your machine (and so your `lianad` need to be connected to a `bitcoind`).

#### Autodetect way (linux only)
If you have a running instance of `lianad` , it should be auto-detected.

```python
from liana_rpc.liana_rpc import LianaRPC

liana = LianaRPC()
```

#### Specifying the socket path
If you are under Windows/MAC or running several `lianad` instances, you'll need to specify the socket path:

```python
from liana_rpc.liana_rpc import LianaRPC

liana = LianaRPC('~/.liana/signet/lianad_rpc')
```

### Get wallet info:
```python
import json
from liana_rpc.liana_rpc import LianaRPC

liana = LianaRPC()

print(json.dumps(liana.get_info(), indent=2))
```

output:

```
{
  "block_height": 153381,
  "descriptors": {
    "main": {
      "change_desc": "wsh(or_i(and_v(v:pkh([c6fb74e6/48'/1'/1'/2']tpubDFJBUNcNBTvAZYp5CteCpbCBfs8GhescLJPfTvcH7jugvFAffTr67BjvZ28g2fqt2bkHYTNTwaC95hx6byTFi8kVQa/1/*),older(20)),or_d(multi(2,[c4fb74e6/48'/1'/0'/2']tpubDE4XEBLMec4eRURN3QGNFGJZcvPT7r1AGELL7P5fbiBp2txJCRfAmNHnjCF1YZsbzkQYZKVpTvRGWLbwYGgFHp6Sb8atSWKyzKsv4dUp1vY/1/*,[a5c6b76e/48'/1'/0'/2']tpubDF5861hj6vR3iJr3aPjGJz4rNbqDCRujQ21mczzKT5SiedaQqNVgHC8HT9ceyxvMFRoPMx4P6HAcL3NZrUPhRUbwCyj3TKSa64bAfnE3sLh/1/*),and_v(v:pkh([a5c6b76e/48'/1'/1'/2']tpubDFhfKfRZcoXt9uMAWCEmtbv5sFaZ3o9bUyQ74Gj1UxxS5MHENpBhMXmc6gfkMXoJnDTfso1Gzyb2DpwpPVeJsgGee1qXAAQ1AhBNqFG6Mwt/1/*),older(10)))))#y4kctn23",
      "multi_desc": "wsh(or_i(and_v(v:pkh([c6fb74e6/48'/1'/1'/2']tpubDFJBUNcNBTvAZYp5CteCpbCBfs8GhescLJPfTvcH7jugvFAffTr67BjvZ28g2fqt2bkHYTNTwaC95hx6byTFi8kVQa/<0;1>/*),older(20)),or_d(multi(2,[c4fb74e6/48'/1'/0'/2']tpubDE4XEBLMec4eRURN3QGNFGJZcvPT7r1AGELL7P5fbiBp2txJCRfAmNHnjCF1YZsbzkQYZKVpTvRGWLbwYGgFHp6Sb8atSWKyzKsv4dUp1vY/<0;1>/*,[a5c6b76e/48'/1'/0'/2']tpubDF5861hj6vR3iJr3aPjGJz4rNbqDCRujQ21mczzKT5SiedaQqNVgHC8HT9ceyxvMFRoPMx4P6HAcL3NZrUPhRUbwCyj3TKSa64bAfnE3sLh/<0;1>/*),and_v(v:pkh([a5c6b76e/48'/1'/1'/2']tpubDFhfKfRZcoXt9uMAWCEmtbv5sFaZ3o9bUyQ74Gj1UxxS5MHENpBhMXmc6gfkMXoJnDTfso1Gzyb2DpwpPVeJsgGee1qXAAQ1AhBNqFG6Mwt/<0;1>/*),older(10)))))#t4nta0mn",
      "receive_desc": "wsh(or_i(and_v(v:pkh([c6fb74e6/48'/1'/1'/2']tpubDFJBUNcNBTvAZYp5CteCpbCBfs8GhescLJPfTvcH7jugvFAffTr67BjvZ28g2fqt2bkHYTNTwaC95hx6byTFi8kVQa/0/*),older(20)),or_d(multi(2,[c4fb74e6/48'/1'/0'/2']tpubDE4XEBLMec4eRURN3QGNFGJZcvPT7r1AGELL7P5fbiBp2txJCRfAmNHnjCF1YZsbzkQYZKVpTvRGWLbwYGgFHp6Sb8atSWKyzKsv4dUp1vY/0/*,[a5c6b76e/48'/1'/0'/2']tpubDF5861hj6vR3iJr3aPjGJz4rNbqDCRujQ21mczzKT5SiedaQqNVgHC8HT9ceyxvMFRoPMx4P6HAcL3NZrUPhRUbwCyj3TKSa64bAfnE3sLh/0/*),and_v(v:pkh([a5c6b76e/48'/1'/1'/2']tpubDFhfKfRZcoXt9uMAWCEmtbv5sFaZ3o9bUyQ74Gj1UxxS5MHENpBhMXmc6gfkMXoJnDTfso1Gzyb2DpwpPVeJsgGee1qXAAQ1AhBNqFG6Mwt/0/*),older(10)))))#kn6q4tpu"
    }
  },
  "network": "signet",
  "rescan_progress": null,
  "sync": 1.0,
  "version": "1.0.0-dev"
}
```

### Generate a new receiving address:
```python
from liana_rpc.liana_rpc import LianaRPC

liana = LianaRPC()

addr = liana.get_new_address()
print(addr)
```
output:


```
tb1qlmdc720pler50uhrf88xdt6chrqtuzrldfkw9727hqdr3e25r4csqc0m9x
```

### List unspent coins:
```python
from liana_rpc.liana_rpc import LianaRPC

liana = LianaRPC()

coins = liana.list_unspent_coins()

for coin in coins:
    print(coin)
```
output:


```
{'amount': 10000, 'block_height': 142843, 'outpoint': '4450583c111e4a2974898e4b5068717f852c5b9e1803531ee2d006aedd2e9e39:0', 'spend_info': None}
{'amount': 10000, 'block_height': 142843, 'outpoint': '4450583c111e4a2974898e4b5068717f852c5b9e1803531ee2d006aedd2e9e39:6', 'spend_info': None}
{'amount': 4607905, 'block_height': 144942, 'outpoint': '9b20145363703a3309166aa1af48d7907cc42dd98d49843ffb24ef909d1da108:1', 'spend_info': None}
{'amount': 10000, 'block_height': 142843, 'outpoint': '4450583c111e4a2974898e4b5068717f852c5b9e1803531ee2d006aedd2e9e39:1', 'spend_info': None}

```

