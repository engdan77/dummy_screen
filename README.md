**dummy_screen**

Usage
```
usage: dummy_screen.py [-h] [--port PORT] [--workdir WORKDIR]

A very simple application for expose a json-socket server easily used for
control text and images being displayed through tool such as NetCat

optional arguments:
  -h, --help         show this help message and exit
  --port PORT        Which port to open for incomming connections
  --workdir WORKDIR  Specify which path to use for temporary files, for
                     example if you like to use a tmpfs in-memory
```


**Samples**

Display a simple large text
```bash
echo '{"text": {"input_text": "Hello World"}}' | nc 127.0.0.1 9999
```

Display a PNG image base64 encoded
```bash
echo "{\"image\": {\"base64_data\": \"$(cat /tmp/testimage.png | base64)\"}}" | nc 127.0.0.1 9999
```

Remotely exit the application
```bash
echo '{"command": "exit"}' | nc 127.0.0.1 9999
```