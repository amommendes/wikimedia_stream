import functools
from config.environment import Configuration
from db.connector import Connector
from db.dao import Dao
from flask import jsonify
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,
)

conf = Configuration()
dao = Dao()
bp = Blueprint('home', __name__)

@bp.route('/')
def home():
    return render_template('index.html')


@bp.route("/count")
def getCount():
    return str(dao.count)

@bp.route("/sum")
def sumLength():
    return str(dao.sumLength)

@bp.route("/countEdits")
def countBySecond():
    return jsonify(dao.countBySecond)