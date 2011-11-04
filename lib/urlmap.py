"""
A generic URL-mapping system.
"""
import re

get = "GET"
put = "PUT"
post = "POST"
delete = "DELETE"

def urlMap(pathHandlerPairs):
    """
    Format is [ [ "/?$", { get: someHandler } ] ]

    Where "someHandler" takes weblib-style Request
    and Response objects.

    :param pathHandlerPairs: list of [ uncompiled regexp, dict ] pairs
    :return: the same list, but with regexps compiled
    """
    return [
        (re.compile(path), handlers)
        for path, handlers in pathHandlerPairs]

