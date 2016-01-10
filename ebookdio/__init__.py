import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

root = lambda p: os.path.join(os.path.dirname(__file__), p)

app = Flask(__name__)
app.debug = True
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + root('ebookdio.db')
db = SQLAlchemy(app)
