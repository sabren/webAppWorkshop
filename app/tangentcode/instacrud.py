"""
InstaCRUD
"""
from functools import wraps
from django.utils import simplejson
from google.appengine.ext import db


class GridModel(db.Model):
    seq = db.IntegerProperty()
    name = db.StringProperty()

    def toDict(self):
        return {
            'url' : "/api/g/%i" % self.key().id(),
            'name': self.name,
        }

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


class CRUDError(Exception):
    pass

def throw(ex):
    raise ex


def jsonify(func):
    @wraps(func)
    def decorated(req, res=None):
        json = simplejson.dumps(func(req, res))
        if res:
            res.write(json)
            res.contentType = "application/json"
        else:
            return simplejson.loads(json)
    return decorated

@jsonify
def list_grids(req, res):
    return list(GridModel.all())


@jsonify
def new_grid(req, res):
    name = req.get('name') or throw(CRUDError("no name given"))
    g = GridModel.gql("WHERE name=:1", name)
    if g.count(): raise CRUDError("%r exists" % name)
    g = GridModel(name=name)
    g.put()
    return g.toDict()


def get_grid_meta(req, res):
    return None


def put_grid_meta(req, res):
    return None


def put_grid_row(req, res):
    return None


def delete_grid(req, res):
    return None


def get_grid_data(req, res):
    return None


def get_grid_row(req, res):
    return None


def delete_grid_row(req, res):
    return None
