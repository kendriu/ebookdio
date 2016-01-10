import os
import sqlite3

from flask import Flask
from flask_bootstrap import Bootstrap

from decorators import templated

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
    with get_db() as db:
        books = db.execute('SELECT * FROM books ORDER BY author').fetchall()
    return {'books': books}

if __name__ == "__main__":
    app.run()
