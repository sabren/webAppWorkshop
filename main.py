#!/usr/bin/env python
# webAppWorkshop for Google App Engine.
# Copyright 2011 Sabren Enterprises, Inc. All Rights Reserved.
"""
This is the main dispatcher for http://*.webappworkshop.com/
"""
from google.appengine.ext.webapp import util
from Cookie import SimpleCookie
import os, sys, logging
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

import weblib, handy

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

    main = findAppMain(req.host)
    eng = AppEngineEngine(script=main)
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


def findAppMain(serverName):
    """
    Given a domain like foo.webappworkshop.com, this
    checks for app/foo/foo.py

    :param serverName: the SERVER_NAME from wsgi
    :return: the imported root module, or None
    """
    if serverName.startswith("localhost"): return None
    if serverName.endswith("localhost"):
        appName = '.'.join(serverName.split('.')[:-1])
    else:
        appName = '.'.join(serverName.split('.')[:-2])
    logging.debug("appName is %r" % appName)
    if os.path.exists("app/%s/%s.py" % (appName, appName)):
        modname = 'app.%s.%s' % (appName, appName)
        exec 'import %s' % modname
        return getattr(eval(modname), 'main')
    else:
        logging.debug("%s is not a valid app" % serverName)
        return None


if __name__ == '__main__':
    if (os.environ["SERVER_NAME"]).endswith("localhost"):
        logging.getLogger().setLevel(logging.DEBUG)
    util.run_wsgi_app(weblib_app)
