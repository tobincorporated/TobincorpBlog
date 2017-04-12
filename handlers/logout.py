from bloghandler import BlogHandler

class Logout(BlogHandler):
    """Page for logging out of a user account"""
    def get(self):
        self.set_logout_cookie()
        self.redirect('/')
