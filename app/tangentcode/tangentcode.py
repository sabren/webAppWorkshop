import logging, re
from app.tangentcode import editor, instacrud, errors

get = "GET"
put = "PUT"
post = "POST"
delete = "DELETE"

urlMap =[(re.compile(path), handlers) for path, handlers in
[
    (r"/$", {
        get: editor.showEditor }),
    (r"/api/g/?$", {
        get: instacrud.list_grids,
        post: instacrud.new_grid}),
    (r"/api/g/(?P<table>\w+)/?$", {
        get: instacrud.get_grid_meta,
        put: instacrud.put_grid_meta,
        post: instacrud.put_grid_row,
        delete: instacrud.delete_grid}),
    (r"/api/g/(?P<table>\w+)/data/?$", {
        get: instacrud.get_grid_data}),
    (r"/api/(?P<table>\w+)/(?P<id>\d+)/?$", {
        get: instacrud.get_grid_row,
        put: instacrud.put_grid_row,
        delete: instacrud.delete_grid_row}),
]]


def main(req, res):
    """
    Dispatch based on the urlMap above.

    :param req:
    :param res:
    :return:
    """
    for path, handlers in urlMap:
        if path.match(req.path):
            if handlers.has_key(req.method):
                method = handlers[req.method]
            else:
                method = errors.err405MethodNotSupported
            break
    else:
        method = errors.err404NotFound
    logging.info("method is: %s", method.__name__)
    return method(req, res)

