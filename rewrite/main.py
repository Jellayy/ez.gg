import webview
import asyncio
import threading

from flask import Flask

from events.ws import websocket_handler
from routes import register_routes
from initialize import lcu


server = Flask(__name__, static_folder='./ui/static', template_folder='./ui/templates')

register_routes(server)


def run_asyncio_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.create_task(websocket_handler())

    thread = threading.Thread(target=run_asyncio_loop, args=(loop,), daemon=True)
    thread.start()

    webview.create_window('EZ.GG Experimental', server, frameless=True, height=760, width=500)
    webview.start(user_agent='EZ.GG Experimental')
