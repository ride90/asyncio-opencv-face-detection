import io
import ssl
import cv2 as cv
import numpy as np
from uuid import uuid4

import filetype
import aiohttp
import aiofiles
from aiohttp import web
import jinja2
import aiohttp_jinja2
from PIL import Image

from camera import VideoCamera


# settings
DEBUG = True
PORT = 8088
FAKE_SSL = True
JINJA2_TEMPLATES_DIR = 'templates'

routes = web.RouteTableDef()


@routes.get('/')
@aiohttp_jinja2.template('index.html')
async def index(request):
    return {}


@routes.get('/ws')
async def ws_handler(request):
    print('[WS] Connection opened')
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    # wait for messages
    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.BINARY:
            np_arr = np.frombuffer(msg.data, dtype=np.uint8)
            np_img = cv.imdecode(np_arr, cv.IMREAD_COLOR)
            np_img = VideoCamera.detect_faces(np_img)

            is_success, im_buf_arr = cv.imencode(".jpg", np_img)
            byte_im = im_buf_arr.tobytes()


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
    if FAKE_SSL:
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.check_hostname = False
        ssl_context.load_cert_chain('certificate/sslcert.crt', 'certificate/sslcert.key')
    web.run_app(app, port=PORT, ssl_context=ssl_context)
