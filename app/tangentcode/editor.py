def showEditor(req, res):
    res.write(open("app/tangentcode/editor.html").read())
