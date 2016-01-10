import logging

from ebookdio import app
from ebookdio.decorators import templated
from ebookdio.models import Book

log = logging.Logger(__file__)
log.addHandler(logging.StreamHandler())


@app.route('/')
@templated()
def home():
    return {'books': Book.query.order_by('title').all()}
