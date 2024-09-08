import webview

from flask import Flask, render_template

from routes import register_routes
from bristle_instance import lcu


server = Flask(__name__, static_folder='./ui/static', template_folder='./ui/templates')

register_routes(server)


if __name__ == '__main__':
    webview.create_window('EZ.GG Experimental', server, frameless=True, height=760)
    webview.start(user_agent='EZ.GG Experimental')
