"""
InstaCRUD
"""
from functools import wraps
from django.utils import simplejson
from google.appengine.ext import db



class GridModel(db.Model):
    seq = db.IntegerProperty()
    name = db.StringProperty()
    cols = db.IntegerProperty()

    def toDict(self):
        return { self.name :[c.toList() for c in self.columns] }

class ColumnModel(db.Model):
    grid = db.ReferenceProperty(GridModel, collection_name="columns")
    seq = db.IntegerProperty()
    name = db.StringProperty()
    type = db.StringProperty()
    help = db.StringProperty()

    def toList(self):
        return [self.type, self.name]

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
        try:
            json = simplejson.dumps(func(req, res))
        except CRUDError, e:
            if not res: raise
            res.addHeader('status', '400 bad request')
            res.contentType = "text/plain"
            res.write(e.message)
            return e
        if res:
            res.write(json)
            res.contentType = "application/json"
        else:
            return simplejson.loads(json)
    return decorated

@jsonify
def list_grids(req, res):
    return [g.toDict() for g in GridModel.all()]


@jsonify
def create_grid(req, res):
    json = simplejson.loads(req.content)
    name = json.get('name') or throw(CRUDError("no name given. expected string"))
    meta = json.get('meta') or throw(CRUDError("no meta given. expected [[string type]]"))
    g = GridModel.gql("WHERE name=:1", name)
    if g.count(): raise CRUDError("%r exists" % name)
    g = GridModel(name=name, cols=0)
    g.put()
    for rowType, rowName in meta:
        r = ColumnModel(parent=g, grid=g, name=rowName, type=rowType)
        r.put()
        g.cols += 1
    g.put()
    return g.toDict()


def get_grid_meta(req, res):
    return None


def put_grid_meta(req, res):
    names = req.get("names", [])
    types = req.get("types", [])
    if len(names) != len(types):
        raise CRUDError("please supply the same number of names and types!")
    if not len(names):
        raise CRUDError("please supply names and types for the columns.")


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
