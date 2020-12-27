from demo.app.server import server
from webview import create_window, start

win = create_window('demo', server)
start(gui='cef', debug=True)
