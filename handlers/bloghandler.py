from functools import wraps
from google.appengine.ext import db
import os
import webapp2
import hmac
import jinja2
from models import User, Entry, Like, Comment

# Secret key used for hashing
secret = 'k8j4dsdf'

template_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ),
                                            '..', 'templates'))
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

def blog_key(name='default'):
    return db.Key.from_path('blogs', name)

def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val

def make_secure_val(val):
    return '%s|%s' % (val, hmac.new(secret, val).hexdigest())

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

# Decorators used to check validity of user actions
def user_logged_in(function):
    @wraps(function)
    def wrapper(self, *a):
        if self.user:
            return function(self, *a)
        else:
            self.redirect("/login?error=You must be logged in first")
            return
    return wrapper

def entry_exists(function):
    @wraps(function)
    def wrapper(self, entry_id):
        key = db.Key.from_path('Entry', int(entry_id), parent=blog_key())
        entry = db.get(key)
        if entry:
            return function(self, entry_id)
        else:
            self.error(404)
            return
    return wrapper

def comment_exists(function):
    @wraps(function)
    def wrapper(self, entry_id, comment_id):
        key = db.Key.from_path('Comment', int(comment_id),
                               parent=blog_key())
        comment = db.get(key)
        if comment:
            return function(self, entry_id, comment_id)
        else:
            self.error(404)
            return
    return wrapper

def user_owns_entry(function):
    @wraps(function)
    def wrapper(self, entry_id):
        key = db.Key.from_path('Entry', int(entry_id), parent=blog_key())
        entry = db.get(key)
        if entry.user_id == self.user.key().id():
            return function(self, entry_id)
        else:
            self.redirect("/" + entry_id +
                          "?error=You can't edit someone else's entry")
            return
    return wrapper

def user_owns_comment(function):
    @wraps(function)
    def wrapper(self, entry_id, comment_id):
        key = db.Key.from_path('Comment', int(comment_id),
                               parent=blog_key())
        comment = db.get(key)
        if comment.user_id == self.user.key().id():
            return function(self, entry_id, comment_id)
        else:
            self.redirect("/" + entry_id +
                          "?error=You can't edit someone else's comment")
            return
    return wrapper

class BlogHandler(webapp2.RequestHandler):
    """
    Handles common functions needed for the blog's handlers
    """
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        params['user'] = self.user
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def set_login_cookie(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    def set_logout_cookie(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))
