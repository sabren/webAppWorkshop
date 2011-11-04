import logging, re
from app.tangentcode import editor
import weblib, instacrud, errors

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
        post: instacrud.create_grid}),
    (r"/api/g/(?P<table>\w+)/?$", {
        get: instacrud.get_grid_meta,
        #put: instacrud.put_grid_meta,
        post: instacrud.create_grid_row,
        #delete: instacrud.delete_grid
        }),
    (r"/api/g/(?P<table>\w+)/data/?$", {
        get: instacrud.get_grid_data}),
    (r"/api/g/(?P<table>\w+)/(?P<id>\d+)/?$", {
        get: instacrud.get_grid_row,
        put: instacrud.put_grid_row,
        delete: instacrud.delete_grid_row}),
]]


#!! pycharm 2 EAP doesn't like for...else
#noinspection PyUnboundLocalVariable
def main(req, res):
    """
    Dispatch based on the urlMap above.

    :type req: weblib.Request
    :type res: weblib.Response
    :return:
    """
    assert isinstance(req, weblib.Request)
    for path, handlers in urlMap:
        match = path.match(req.path)
        if match:
            if handlers.has_key(req.method):
                req.pathArgs = match.groupdict()
                method = handlers[req.method]
            else:
                method = errors.err405MethodNotSupported
            break
    else:
        method = errors.err404NotFound
    logging.info("method is: %s", method.__name__)
    return method(req, res)

