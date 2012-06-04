#!/usr/bin/env python
# webAppWorkshop for Google App Engine.
# Copyright 2011 Sabren Enterprises, Inc. All Rights Reserved.
"""
This is the main dispatcher for http://*.webappworkshop.com/
"""
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from Cookie import SimpleCookie
import os, sys, logging

sys.path.extend([os.path.join(os.path.dirname(__file__), path)
                for path in ['lib','libcopy']])

import weblib, handy
import ERR, REST, CRUD

class AppEngineEngine(weblib.Engine):
    """
    This strips a bunch of CGI-specific junk out of weblib,
    so we can use it on App Engine.
    """
    # TODO clean Engine up to be fully wsgi-compliant so we don't need this!
    def _exec(self, script):
        if script:
            script(self.request, self.response)
        else:
            self.response.addHeader("status", "404 Not Found")
            self.response.write(handy.trim(
                """
                <!doctype html>
                <html>
                <head>
                  <title>404 Not Found</title>
                </head>
                <body>
                  <h1>404 Not Found</h1>
                  <p>There is no app at <strong>%s</strong>.</p>
                </body>
                <html>
                """) % self.request.host)

    def setPathInfo(self):
        self.request.pathInfo = self.request.path

    def chdir(self):
        pass

    def runDotWeblibPy(self):
        pass


def weblib_app(environ, start_response):

    import pprint
    pprint.pprint(environ)

    req = weblib.Request(
        method = environ["REQUEST_METHOD"],
        host = environ["SERVER_NAME"],
        path = environ["SCRIPT_NAME"] + environ["PATH_INFO"],
        query = weblib.RequestData(environ["QUERY_STRING"]),
        form = None,
        cookie = SimpleCookie(environ.get("HTTP_COOKIE", "")),
        content = environ["wsgi.input"].read(
            int(environ.get("CONTENT_LENGTH", 0) or 0)),
        remoteAddress = environ["REMOTE_ADDR"],
    )

    req.ob = webapp.Request(environ)

    urls = getAppURLs(req.host)
    main = getAppMain(urls, req)

    eng = AppEngineEngine(script=main, request=req)
    eng.run()

    response = eng.response
    out = weblib.OutputDecorator(eng)

    status = "500 Internal Server Error" if eng.hadProblem() else "200 OK"
    headers = [("Content-Type", response.contentType)]
    for k,v in response.headers:
        if k.lower() == "status":
            status = v
        else:
            headers.append((k,v))

    start_response(status, headers)
    yield out.getBody()


def getAppURLs(serverName):
    """
    Given a domain like foo.webappworkshop.com,
    this builds a map of the urls.

    :param serverName: the SERVER_NAME from wsgi
    :return: the imported root module, or None
    """
    universal_api = REST.urlMap(
    [
        (r"/api/g/?$",
        {
            REST.get: CRUD.list_grids,
            REST.post: CRUD.create_grid
        }),
        (r"/api/g/(?P<table>\w+)/?$",
        {
            REST.get: CRUD.get_grid_meta,
            #put: CRUD.put_grid_meta,
            REST.post: CRUD.create_grid_row,
            #delete: CRUD.delete_grid
        }),
        (r"/api/g/(?P<table>\w+)/data/?$",
        {
            REST.get: CRUD.get_grid_data
        }),
        (r"/api/g/(?P<table>\w+)/(?P<id>\d+)/?$",
        {
            REST.get: CRUD.get_grid_row,
            REST.put: CRUD.put_grid_row,
            REST.delete: CRUD.delete_grid_row
        }),
    ])

    res = universal_api
    if serverName.startswith("localhost"): return None
    if serverName.endswith("localhost"):
        appName = '.'.join(serverName.split('.')[:-1])
    else:
        appName = '.'.join(serverName.split('.')[:-2])
    logging.debug("appName is %r" % appName)
    if os.path.exists("app/%s/%s.py" % (appName, appName)):
        modname = 'app.%s.%s' % (appName, appName)
        exec 'import %s' % modname
        extras = getattr(eval(modname), 'urls', [])
        res.extend(extras)
        return res
    else:
        logging.debug("%s is not a valid app" % serverName)
        return res


def getAppMain(urlMap, req):
    """
    :type urlMap: list of regexp->dict pairs
    :type req: weblib.Request
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
                method = ERR.err405MethodNotSupported
            break
    else:
        method = ERR.err404NotFound
    logging.info("method is: %s", method.__name__)
    return method




if __name__ == '__main__':
    if os.environ["SERVER_NAME"].endswith("localhost"):
        logging.getLogger().setLevel(logging.DEBUG)
    util.run_wsgi_app(weblib_app)
