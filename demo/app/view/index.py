from flask import Blueprint, render_template, request, redirect

from demo.app.api import api

blueprint = Blueprint('index', __name__)


@blueprint.route('/')
def index():
    api.get_recommend_songs()
    if api.profile:
        resp = api.get_user_playlist()
        active_playlist = request.args.get('playlist', resp['playlist'][0]['id'])
        playlist_detail = api.get_playlist_detail(active_playlist)
        return render_template('index.html',
                               current_user=api.profile, playlists=resp['playlist'],
                               playlist_detail=playlist_detail)
    else:
        return render_template('index.html')


@blueprint.route('/login', methods=['POST'])
def login():
    api.login(request.form['username'], request.form['password'])
    return redirect('/', 301)
