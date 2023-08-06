# modbus-tcp-server

[![PyPI](https://img.shields.io/pypi/pyversions/smok.svg)](https://pypi.python.org/pypi/smok)
[![PyPI version](https://badge.fury.io/py/smok.svg)](https://badge.fury.io/py/smok)
[![PyPI](https://img.shields.io/pypi/implementation/smok.svg)](https://pypi.python.org/pypi/smok)
[![Wheel](https://img.shields.io/pypi/wheel/smok.svg)](https://pypi.org/project/smok/)


A thread-based MODBUS TCP server for testing purposes.

# Installation

Just type 

```bash
pip install modbus-tcp-server
```

And to run it

```bash
modbus-tcp-server 127.0.0.1
```

Just run it without any arguments to see the command line.

# Limitations

So far commands 15 (Force Multiple Coils) 
and 16 (Preset Multiple Registers) are unsupported.

# Custom usage

To implement a custom provider ModbusTCPServer, just extend
[BaseDataSource](modbus_tcp_server/data_source/base.py) 
to provide data of your choosing and launch it that way: 

```python
from modbus_tcp_server.network import AcceptThread
from modbus_tcp_server.data_source import BaseDataSource

class CustomDB(BaseDataSource):
    ...

c_db = CustomDB()

at = AcceptThread('0.0.0.0', 502, c_db).start()
```
