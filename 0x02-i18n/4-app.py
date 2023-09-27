#!/usr/bin/env python3
"""
App FLASK
"""
from flask import Flask, render_template, request
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


@babel.locale_selector
def get_locale():
    """
    Best match language
    """
    if 'locale' in request.args:
        requested_locale = request.args.get('locale')
        if requested_locale in app.config['LANGUAGES']:
            return requested_locale

    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route("/", methods=["GET"], strict_slashes=False)
def home():
    # Generate URLs with 'locale' parameter
    fr_url = url_for('home', locale='fr')
    en_url = url_for('home', locale='en')

    return render_template('4-index.html', fr_url=fr_url, en_url=en_url)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
