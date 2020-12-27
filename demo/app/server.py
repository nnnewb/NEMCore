from os import getenv
from flask import Flask

from demo.app.const import gui_dir
from demo.app.view.index import blueprint as index_blueprint

server = Flask(__name__, static_folder=gui_dir, template_folder=gui_dir)
server.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1  # disable caching
server.config['DEBUG'] = bool(getenv('DEBUG', None))

server.register_blueprint(index_blueprint)
