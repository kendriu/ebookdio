#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask.ext.script import Manager

from ebookdio import db
from ebookdio.models import Book
from ebookdio.views import app
from scripts.match import get_matched_books

manager = Manager(app)


@manager.command
def db_populate():
    db.drop_all()
    db.create_all()
    books = get_matched_books()
    for book in books:
        book = Book(title=book['title'], author=book['author'])
        db.session.add(book)
    db.session.commit()


if __name__ == "__main__":
    manager.run()
