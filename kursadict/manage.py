# manage.py
# -*- encoding:utf-8 -*-

from flask import Flask
from flaskext.actions import Manager
from neahtta import app

manager = Manager(app, default_server_actions=True)

if __name__ == "__main__":
    app.caching_enabled = True
    manager.run()

