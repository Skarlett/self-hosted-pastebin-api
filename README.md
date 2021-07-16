# self-hosted-pastebin-api
---
This project runs an http server, that has similar end goals as pastebin.
The client uploads text, and that text is collected, and reflected on the server with a unique URL.

```sh
transfer() {
  curl -F paste=@$1 http://your_host:8080/submit
}
```

## Running the server
```
python3 app.py --port 8080
```

## Synopsis
```
NAME
    app.py

SYNOPSIS
    app.py <flags>

FLAGS
    --serve=SERVE
        Directory to upload text dumps.
        Default: '/tmp/pastes'
    
    --port=PORT
        Port to run http server on.
        Default: 8080
    
    --interface=INTERFACE
        IP host interface. 
        Example: 127.0.0.1
        Default: '0.0.0.0'
    
    --log=LOG
        File path to write log file.
        Example: http.log     
        Default: None
    
    --host=HOST
        Host defines how the server believes other clients will connect back it.
        Example: pastes.lan
        Default: None
```