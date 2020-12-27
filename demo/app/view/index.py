from flask import Blueprint, render_template

blueprint = Blueprint('index', __name__)


@blueprint.route('/')
def index():
    return render_template('index.html')
