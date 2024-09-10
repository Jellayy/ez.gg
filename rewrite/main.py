import webview
import asyncio
import threading
import os
import time

from flask import Flask

from events.lcu_ws import websocket_handler
from routes import register_routes
from sse import register_routes as register_sse_routes
from initialize import lcu


server = Flask(__name__, static_folder='./ui/static', template_folder='./ui/templates')

register_routes(server)
register_sse_routes(server)


def run_asyncio_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


# This closes the app pretty harshly and causes an error on exit
# Maybe look at a better way to do this
# We have to do this because a connection is maintained in sse.py
def shutdown_app():
    time.sleep(0.1)
    os._exit(0)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.create_task(websocket_handler())

    thread = threading.Thread(target=run_asyncio_loop, args=(loop,), daemon=True)
    thread.start()

    window = webview.create_window('EZ.GG Experimental', server, frameless=True, height=760, width=500)
    window.events.closed += shutdown_app
    webview.start(user_agent='EZ.GG Experimental')
