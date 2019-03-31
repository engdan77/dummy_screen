
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