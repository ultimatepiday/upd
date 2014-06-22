#!/usr/bin/python
#http://flask.pocoo.org/docs/patterns/packages/

import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask.ext.mustache import FlaskMustache

app = Flask(__name__)
app.config.from_pyfile('default_settings.cfg')
app.config.from_envvar('UPD_SETTINGS', silent=True)

FlaskMustache(app)

import upd.views
