import REST, LOGIN

class OutVar: value = None

def main(req, res):
    """
    :param weblib.Request req
    :param weblib.Response res
    """
    out = OutVar()
    if LOGIN.check(req, res, out):
        res.write(
            """
            <!doctype html>
            <html>
            <head>
              <title>webAppWorkshop</title>
            </head>
            <body>
              <h1>Hello, %s</h1>
              <p>Greetings from <strong>%s</strong>!</p>
            </body>
            </html>
            """
            % ( out.value.nickname(), req.host ))


urls = REST.urlMap([
    (r"/$", {
        REST.get: main }),
    ])
