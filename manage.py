#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask.ext.script import Manager
from ebookdio.app import app

manager = Manager(app)


@manager.command
def populate_db():
    pass

if __name__ == "__main__":
    manager.run()
