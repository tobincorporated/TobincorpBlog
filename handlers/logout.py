
from google.appengine.ext import db

from bloghandler import BlogHandler
from models import User
from models import Entry
from models import Comment

def blog_key(name='default'):
    return db.Key.from_path('blogs', name)

class Logout(BlogHandler):
    """Page for logging out of a user account"""
    def get(self):
        self.set_logout_cookie()
        self.redirect('/')
