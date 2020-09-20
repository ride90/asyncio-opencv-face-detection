import os
import ssl
import cv2 as cv
import numpy as np
from distutils.util import strtobool

import aiohttp
from aiohttp import web
import jinja2
import aiohttp_jinja2

from camera import VideoCamera


# settings
DEBUG = strtobool(os.environ.get('DEBUG', 'True'))
PORT = int(os.environ.get('PORT', 8088))
SSL = strtobool(os.environ.get('SSL', 'True'))
SSL_CRT_PATH = os.environ.get('SSL_CRT_PATH', 'certificate/sslcert.crt')
SSL_KEY_PATH = os.environ.get('SSL_KEY_PATH', 'certificate/sslcert.key')
REVERSE_PROXY_WS_URL = os.environ.get('REVERSE_PROXY_WS_URL', 'wss://0.0.0.0:8088/ws')
JINJA2_TEMPLATES_DIR = 'templates'

routes = web.RouteTableDef()


@routes.get('/')
@aiohttp_jinja2.template('index.html')
async def index(request):
    return {
        "WS_URL": REVERSE_PROXY_WS_URL
    }


@routes.get('/ws')
async def ws_handler(request):
    print('[WS] Connection opened')
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    # wait for messages
    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.BINARY:
            # convert image binary to numpy array
            np_arr = np.frombuffer(msg.data, dtype=np.uint8)
            # convert np array to np img (matrix)
            np_img = cv.imdecode(np_arr, cv.IMREAD_COLOR)
            # detect faces
            np_img = VideoCamera.detect_faces(np_img)
            # encode img back to byte
            is_success, im_buf_arr = cv.imencode(".jpg", np_img)
            byte_im = im_buf_arr.tobytes()
            # send to client
            await ws.send_bytes(byte_im)
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print(f'[WS] Connection closed with exception {ws.exception()}')

    print('[WS] Connection closed')

    return ws


app = web.Application(debug=DEBUG)
app.add_routes(routes)
aiohttp_jinja2.setup(
    app,
    loader=jinja2.FileSystemLoader(JINJA2_TEMPLATES_DIR)
)

if __name__ == '__main__':
    if SSL:
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.check_hostname = False
        ssl_context.load_cert_chain(SSL_CRT_PATH, SSL_KEY_PATH)
        web.run_app(app, port=PORT, ssl_context=ssl_context)
    else:
        web.run_app(app, port=PORT)
