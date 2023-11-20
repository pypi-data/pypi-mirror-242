# py-valid-proxy

## В работе

### Installation

```
pip install py-valid-proxy
```

### Usage

``` python
from py_valid_proxy import valid_proxy

"""Valid proxy server ('alive' or 'dead')

Parameters
----------
host : str
    IP Address
port : int
    Port
scheme: str, optional
    Scheme (default is 'http')
timeout: int, optional
    Connect timeout is number of seconds (default is 5 sec.)
Returns
-------
    None if proxy is 'dead'
    dict if proxy is 'alive'
    {
        "scheme": str, # http, https
        "host": str,
        "port": int,
        "export_address": list[str],
        "anonymity": str, # transparent, anonymous, high_anonymous # noqa
        "country": str # ISO Code 
        "response_time": float
    }
"""
proxy_info = valid_proxy('8.219.97.248', 80, 'https', 10)
if proxy_info:
	print('is alive')
else:
	print('is dead')
```

[![asciicast](https://asciinema.org/a/hzaN1Z147zqrFqrk8s2299ve1.svg)](https://asciinema.org/a/hzaN1Z147zqrFqrk8s2299ve1)