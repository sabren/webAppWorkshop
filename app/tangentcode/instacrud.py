"""
InstaCRUD
"""
from functools import wraps
from django.utils import simplejson
from google.appengine.ext import db


class GridModel(db.Model):
    seq = db.IntegerProperty()
    name = db.StringProperty()

class ColumnModel(db.Model):
    grid = db.ReferenceProperty(GridModel, collection_name="cols")
    seq = db.IntegerProperty()
    name = db.StringProperty()
    type = db.StringProperty()
    help = db.StringProperty()

class RowModel(db.Expando):
    grid = db.ReferenceProperty(GridModel, collection_name="rows")
    seq = db.IntegerProperty()
    json = db.StringProperty()


def jsonify(func):
    @wraps(func)
    def decorated(req, res):
        res.contentType = "application/json"
        simplejson.dump(func(req, res), res)
    return decorated

@jsonify
def list_grids(req, res):
    return list(GridModel.all())


@jsonify
def new_grid(req, res):
    return dict(url="/api/g/%i" % g.key().id())


def get_table_meta(req, res):
    return None


def put_table_meta(req, res):
    return None


def put_table_row(req, res):
    return None


def delete_table(req, res):
    return None


def get_table_data(req, res):
    return None


def get_table_row(req, res):
    return None


def delete_table_row(req, res):
    return None