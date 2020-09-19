# Detect face using WebRTC, Websockets, Asyncio and OpenCV
Minimal app which sends webcamera's video from the browser via websockets to the aiohttp server (asyncio), handles it and sends back. 


## How it works

WebCamera > Browser (WebRTC) > WebSocket (Blob) > Server -> OpenCV -> Websocket -> Browser

### Note
You need to setup a self signed SSL certificate to allow browser access a camera. See [this line](https://github.com/ride90/asyncio-opencv-face-detection/blob/master/main.py#L67) 

## Demo

![Demo](demo.png "Demo")
