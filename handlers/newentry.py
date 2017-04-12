
from google.appengine.ext import db
from bloghandler import BlogHandler
from models import Entry, User


def blog_key(name='default'):
    return db.Key.from_path('blogs', name)

class NewEntry(BlogHandler):
    """Page for writing a new blog entry"""
    def get(self):
        if self.user:
            self.render("newentry.html")
        else:
            self.redirect("/login")

    def post(self):
        if not self.user:
            self.redirect('/')

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
