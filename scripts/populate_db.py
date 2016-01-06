#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sqlite3

from match import get_matched_books
from utils import ROOT


def main():
    db_file = os.path.join(ROOT, 'ebookdio', 'ebookdio.db')
    try:
        os.remove(db_file)
    except OSError:
        pass
    db = sqlite3.connect(db_file)
    c = db.cursor()
    c.execute('CREATE TABLE books (title, author)')
    books = get_matched_books()
    for book in books:
        c.execute(
            u'INSERT INTO books VALUES ("{title}", "{author}")'.format(**book))


if __name__ == "__main__":
    main()
