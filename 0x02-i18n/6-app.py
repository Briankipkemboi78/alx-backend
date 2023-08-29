#!/usr/bin/env python3
"""
App FLASK
"""
from flask import Flask, render_template, request, g
from flask_babel import Babel, gettext


class Config:
    """
    Config class
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
babel = Babel(app)

app.config.from_object(Config)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


@babel.localeselector
def get_locale():
    """
    Best match language
    """
    # Locale from URL parameters
    locale = request.args.get("locale")
    if locale in app.config['LANGUAGES']:
        return locale
    # Locale from user settings
    user_id = request.args.get('login_as')
    if user_id:
        try:
            locale = users[int(user_id)]['locale']
            if locale in app.config['LANGUAGES']:
                return locale
        except Exception:
            pass
    # Locale from request header
    locale = request.headers.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale
    # Default locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


def get_user():
    """
    get user id
    """
    if request.args.get('login_as'):
        try:
            return users[int(request.args.get('login_as'))]
        except Exception:
            return None
    else:
        return None


@app.route("/", methods=["GET"], strict_slashes=False)
def home():
    """
    home route
    return: template
    """
    return render_template('6-index.html')


@app.before_request
def before_request():
    """
    Before_request handler
    """
    g.user = get_user()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
