# hashell-py
Python bindings for hashell (see https://github.com/Grisshink/hashell)

## Example
```python
from hashell import hash_string

print(hash_string('some value', 16)) # 5149710603511119
```

## Building
```bash
python -m venv env
source env/bin/activate
pip install maturin
maturin develop
```

This should install hashell-py library in your python environment
