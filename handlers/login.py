
from google.appengine.ext import db

from bloghandler import BlogHandler
from models import User



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
