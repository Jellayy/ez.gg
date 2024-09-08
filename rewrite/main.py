from flask import Flask
import webview

server = Flask(__name__, static_folder='./assets', template_folder='./templates')

@server.route("/")
def hello_world():
    return "Hello, World!"

if __name__ == '__main__':
    webview.create_window('Flask example', server)
    webview.start()

