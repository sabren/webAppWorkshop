def main(req, res):
    """
    :param weblib.Request req
    :param weblib.Response res
    """
    res.write(
        """
        <!doctype html>
        <html>
        <head>
          <title>webAppWorkshop</title>
        </head>
        <body>
          <h1>Hello, World</h1>
          <p>Greetings from <strong>%s</strong>!</p>
        </body>
        </html>
        """
        % req.host )
