## DataClient

### Introduction
this is a request tool which packaging method server

### Usage
```python
from stormer import Requester

# init Requester instance
requester = Requester(
    "https://www.baidu.com", 
    redis_url="redis://127.0.0.1:6379/0", 
    # redis_nodes="127.0.0.1:7000,127.0.0.1:7001,127.0.0.1:7002", 
    # redis_password="",
    timeout=30, # in seconds，global cache timeout
    # headers={"Content-Type": "text/html;charset=utf8"},
    encoding='utf8'
)

# open debug
requester.set_debugging()

# register request function
requester.register(
    action="get", 
    func="bd_index", 
    uri="/", 
    timeout=5  # in second, this requester cache timeout
)

# execute function
rlt = requester.bd_index()
r_byte = rlt.bytes
print(rlt.data)
print(rlt.resp)
```




