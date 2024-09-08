from flask import Flask, render_template
import webview

server = Flask(__name__, static_folder='./ui/static', template_folder='./ui/templates')

@server.route("/")
def hello_world():
    return render_template('index.html')

@server.route('/exit', methods=['POST'])
def exit():
    print("exit called")
    webview.windows[0].destroy()
    return '', 204

@server.route('/minimize', methods=['POST'])
def minimize():
    print("minimize called")
    webview.windows[0].minimize()
    return '', 204

if __name__ == '__main__':
    webview.create_window('EZ.GG Experimental', server, frameless=True, height=760)
    webview.start(user_agent='EZ.GG Experimental')
