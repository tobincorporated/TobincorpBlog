
from google.appengine.ext import db

from bloghandler import BlogHandler
from models import User
from models import Entry
from models import Comment

def blog_key(name='default'):
    return db.Key.from_path('blogs', name)

class Login(BlogHandler):
    """Page for logging into a user account"""
    def get(self):
        self.render('login.html', error=self.request.get('error'))

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username, password)
        if u:
            self.set_login_cookie(u)
            self.redirect('/')
        else:
            msg = 'Invalid login'
            self.render('login.html', error=msg)
