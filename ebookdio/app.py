import logging
import os
import sqlite3

from decorators import templated
from flask import Flask
from flask_bootstrap import Bootstrap

log = logging.Logger(__file__)
log.addHandler(logging.StreamHandler())

root = lambda p: os.path.join(os.path.dirname(__file__), p)


def get_db():
    return sqlite3.connect(root('ebookdio.db'))


def create_app():
    app = Flask(__name__)
    app.debug = True
    Bootstrap(app)
    return app

app = create_app()


@app.route('/')
@templated()
def home():
    books = get_books()
    return {'books': books}


def get_books():
    with get_db() as db:
        books = db.execute('SELECT * FROM books ORDER BY author').fetchall()
    result = []
    for title, author in books:
        max_len = 30
        if len(title) > max_len:
            title = title[:max_len] + '...'
        result.append((title, author))

    return result


if __name__ == "__main__":
    app.run()
