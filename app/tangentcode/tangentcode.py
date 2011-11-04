"""
URL map for tangentcode.
"""
from app.tangentcode import editor
from urlmap import *

urls = urlMap([
    (r"/$", {
        get: editor.showEditor }),
    ])
