import os
import logging
import sys
import traceback

from requests_oauthlib import OAuth2Session
from flask import Flask, request, redirect, session, url_for
from flask.json import jsonify

app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY', 'secretkey')
# Getting indentification variables to the JawUp API
client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')

# Getting some configuration variables defined in file.cfg
app.config.from_pyfile("file.cfg")
scope = app.config.get('SCOPE', 'extended_read')
token_url = app.config.get('TOKEN_URL')
authorization_base_url = app.config.get('AUTHORIZATION_BASE_URL')
redirect_base_url = app.config.get('REDIRECT_BASE_URL')

@app.route("/")
def main():
    return "Hello marvelous"

@app.route("/about")
def about():
    return "about page"

@app.route("/loginjaw")
def login():
    jawUp = OAuth2Session(client_id=client_id, scope=scope, redirect_uri=redirect_base_url + url_for('oauth_redirect'))
    authorization_url, state = jawUp.authorization_url(authorization_base_url)
    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state
    return redirect(authorization_url)

@app.route("/redirect")
def oauth_redirect():
    jawUp = OAuth2Session(client_id=client_id)
    code = request.args.get("code")
    state = request.args.get("state")
    token = jawUp.fetch_token(token_url=token_url, code=code, state=state, client_secret=client_secret, authorization_response=request.url)
    return jsonify(jawUp.get('https://jawbone.com/nudge/api/v.1.1/users/@me/moves').json())

if __name__ == "__main__":
    app.run(debug = True)
