**WORK IN PROGESS**

# Extreme EXOS asyncio Client

This repository contains an Extreme EXOS asyncio client, support for both
JSON-RPC and RESTCONF options.

For reference on the EXOS JSON-RPC, refer to [this
document](https://documentation.extremenetworks.com/app_notes/MMI/121152_MMI_Application_Release_Notes.pdf).

For reference on the EXOS OpenConfig support, refer to [this
document](https://api.extremenetworks.com/EXOS/ProgramInterfaces/RESTCONF/RESTCONF.html
).

### Device Configuration

In order to access the EXOS device via API you must enable the web server
feature using either http or https.

```text
enable web https
```

### JSON-RPC Usage

```python
from aioexos.jsonrpc import Device

dev = Device(host='myhostname', username='user', password='Random')
show_one = await dev.cli('show switch')
show_many = await dev.cli(['show switch', 'show version'])

# get text instead of JSON/dict

show_text = await dev.cli('show switch', text=True)
```

### RESTCONF Usage

```python
from aioexos.restconf import Device

dev = Device(host='myhostname', username='user', password='Random')

# login step required for session authentication

await dev.login()

# execute commands providing the restconf URL, supports all request methods
# (GET, POST, etc.)

res = await dev.get('/openconfig-system:system')

# close connection when done with commands
await dev.aclose()
```

