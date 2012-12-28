from functools import wraps
from google.appengine.api import users

# based on https://developers.google.com/appengine/articles/openid#ex

def check(req, res, out):
    """
    usage: if login.check(req, res, out): out.user ...

    :param req:
    :param res:
    :return:
    """
    out.value = users.get_current_user()
    if out.value: result = True
    else: show_login_form(res); result = False
    return result

providers = {
    'Google'   : 'https://www.google.com/accounts/o8/id',
    'Yahoo'    : 'yahoo.com',
    'MySpace'  : 'myspace.com',
    'AOL'      : 'aol.com',
    'MyOpenID' : 'myopenid.com'
}

def show_login_form(res):
    res.write('Hello world! Sign in at: ')
    for name, uri in providers.items():
        res.write('[<a href="%s">%s</a>]' % (
            users.create_login_url(federated_identity=uri), name))
