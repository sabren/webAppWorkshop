
def err405MethodNotSupported(req, res):
    res.addHeader("Status", 405)
    res.write("405 Method Not Supported")


def err404NotFound(req, res):
    res.addHeader("Status", 404)
    res.write("404 not found")