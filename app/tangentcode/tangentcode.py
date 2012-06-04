"""
URL map for tangentcode.
"""
from app.tangentcode import editor
import REST

urls = REST.urlMap([
    (r"/$", {
        REST.get: editor.showEditor }),
])
