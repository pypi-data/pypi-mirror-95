![test](https://github.com/rabizao/oka/workflows/test/badge.svg)
[![codecov](https://codecov.io/gh/rabizao/oka/branch/main/graph/badge.svg)](https://codecov.io/gh/rabizao/oka)

# Client for OKA repository

Install
-------

    sudo apt install python3.8-venv python3.8-dev python3.8-distutils # For Debian-like systems.
    git clone https://github.com/rabizao/oka.git
    cd oka
    python3.8 -m venv venv
    source venv/bin/activate
    pip install -e .

Usage
---

**Transfering data**
<details>
<p>

```python3

from oka import oka
from aiuna.step.dataset import dataset
import sys

from tatu.auth import gettoken

oka.url = "http://localhost:5000"
oka.token = gettoken(oka.url, *sys.argv[1:]) if len(sys.argv) == 3 else "no token yet"
data = dataset.data
did = data.id

# Object approach.
oka << data
d = oka(did)
print(d.uuid)
"""
Please login before.
Username to connect to OKA: 00ptEh8jeD4BOtwv0thXenF
"""
```

```python3

# Object "@" approach.
d = did @ oka
print(d.id)
"""
00ptEh8jeD4BOtwv0thXenF
"""
```

```python3

# Function approach.
from oka.io import send, get
send(data, url="http://localhost:5000")
d = get(did, url="http://localhost:5000")
print(d.uuid)
"""
[Error] You have already uploaded the dataset with OID 00ptEh8jeD4BOtwv0thXenF.
00ptEh8jeD4BOtwv0thXenF
"""
```


</p>
</details>
