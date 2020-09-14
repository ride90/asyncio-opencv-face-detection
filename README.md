# Detect face using WebRTC, Websockets, Asyncio and OpenCV
Minimal app which sends webcamera's video from the browser via websockets to the aiohttp server (asyncio), handles it and sends back. 


## How it works

WebCamera > Browser (WebRTC) > WebSocket (Blob) > Server -> OpenCV -> Websocket -> Browser

## Demo

![Demo](demo.png "Demo")