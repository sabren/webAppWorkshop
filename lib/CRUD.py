"""
CRUD: a generic data store and REST API.
"""
import json
from functools import wraps
from google.appengine.ext import db

class GridModel(db.Model):
    seq = db.IntegerProperty()
    name = db.StringProperty()
    colCount = db.IntegerProperty(default=0)
    rowCount = db.IntegerProperty(default=0)

    def toData(self):
        return {
            "grid": self.name,
            "meta": [c.toData() for c in self.columns],
            "rowCount": self.rowCount }

class ColumnModel(db.Model):
    grid = db.ReferenceProperty(GridModel, collection_name="columns")
    seq = db.IntegerProperty()
    name = db.StringProperty()
    type = db.StringProperty()
    help = db.StringProperty()

    def toData(self):
        return [self.type, self.name]

class RowModel(db.Expando):
    grid  = db.ReferenceProperty(GridModel, collection_name="rows")
    seq   = db.IntegerProperty()
    json  = db.StringProperty()

    def toData(self):
        data = json.loads(self.json)
        data['seq'] = self.seq
        data['id'] = self.key().id()
        return data


class CRUDError(Exception):
    pass

def throw(ex):
    raise ex


def jsonify(func):
    @wraps(func)
    def decorated(req, res=None):
        try:
            asJson = json.dumps(func(req, res))
        except LookupError as e:
            if not res: raise
            res.addHeader('status', '404 not found')
            res.contentType = "text/plain"
            res.write(e.message)
            return e
        except CRUDError as e:
            if not res: raise
            res.addHeader('status', '400 bad request')
            res.contentType = "text/plain"
            res.write(e.message)
            return e
        if res:
            res.write(asJson)
            res.contentType = "application/json"
        else:
            return json.loads(asJson)
    return decorated

@jsonify
def list_grids(req, res):
    return [g.toData() for g in GridModel.all()]


@jsonify
def create_grid(req, res):
    data = json.loads(req.content)
    name = data.get('name') or throw(CRUDError("no name given. expected string"))
    meta = data.get('meta') or throw(CRUDError("no meta given. expected [[string type]]"))
    g = GridModel.gql("WHERE name=:1", name)
    if g.count(): raise CRUDError("%r already exists" % name)
    g = GridModel(name=name, cols=0)
    g.put()
    for rowType, rowName in meta:
        r = ColumnModel(parent=g, grid=g, name=rowName, type=rowType)
        r.put()
        g.colCount += 1
    g.put()
    return g.toData()


def gridFromPath(req):
    """
    Build a Grid from the URL path.
    """
    name = req.pathArgs.get("table") or throw(CRUDError("no table name given. expected string"))
    g = GridModel.gql("WHERE name=:1", name)
    if not g.count():
        raise CRUDError("%r doesn't exist" % name)
    return g[0]

@jsonify
def get_grid_meta(req, res):
    g = gridFromPath(req)
    return g.toData()


def put_grid_meta(req, res): # TODO : put_grid_meta
    names = req.get("names", [])
    types = req.get("types", [])
    if len(names) != len(types):
        raise CRUDError("please supply the same number of names and types!")
    if not len(names):
        raise CRUDError("please supply names and types for the columns.")
    raise NotImplementedError()


@jsonify
def create_grid_row(req, res):
    data = json.loads(req.content) # make sure it parses
    dump = json.dumps(data)
    g = gridFromPath(req)
    def txn():
        g.rowCount += 1
        row = RowModel(parent=g, grid=g, json=dump, seq = g.rowCount)
        g.put()
        row.put()
        return row
    row = db.run_in_transaction(txn)
    return row.toData()


def delete_grid(req, res):
    raise NotImplementedError()

@jsonify
def get_grid_data(req, res):
    g = gridFromPath(req)
    return [row.toData() for row in sorted(g.rows, lambda a,b: cmp(a.seq, b.seq))]


def rowFromPath(req):
    g = gridFromPath(req)
    rid = long(req.pathArgs.get("id"))
    row = RowModel.get_by_id(rid, parent=g)
    if not row: raise LookupError("No %s with ID %s" % (g.name, rid))
    return row


@jsonify
def get_grid_row(req, res):
    row = rowFromPath(req)
    return row.toData()

@jsonify
def put_grid_row(req, res):
    row = RowModel.get_by_id(int(req.pathArgs.get("id")))
    row.json = req.content
    return row.toData()


@jsonify
def delete_grid_row(req, res):
    row = rowFromPath(req)
    g = row.grid
    def txn():
        row.delete()
        g.rowCount -= 1
        g.put()
    db.run_in_transaction(txn)
    return g.toData()
