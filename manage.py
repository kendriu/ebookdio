#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ebookdio.app import app
from flask.ext.script import Manager

manager = Manager(app)


@manager.command
def populate_db():
    print "Use scripts/populate_db.py"


if __name__ == "__main__":
    manager.run()
