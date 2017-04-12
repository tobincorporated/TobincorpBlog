
from google.appengine.ext import db
from bloghandler import BlogHandler, user_logged_in, blog_key
from models import Entry

class NewEntry(BlogHandler):
    """Page for writing a new blog entry"""
    @user_logged_in
    def get(self):
        self.render("newentry.html")

    @user_logged_in
    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            p = Entry(parent=blog_key(), user_id=self.user.key().id(),
                     subject=subject, content=content)
            p.put()
            self.redirect('/' + str(p.key().id()))
        else:
            error = "subject and content, please!"
            self.render("newentry.html", subject=subject,
                        content=content, error=error)
