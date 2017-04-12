
from google.appengine.ext import db
from bloghandler import BlogHandler
from models import Entry, User



def blog_key(name='default'):
    return db.Key.from_path('blogs', name)

class EditEntry(BlogHandler):
    """Page for editing a blog entry"""
    def get(self, entry_id):
        if self.user:
            key = db.Key.from_path('Entry', int(entry_id), parent=blog_key())
            entry = db.get(key)
            if entry.user_id == self.user.key().id():
                self.render("editentry.html", subject=entry.subject,
                            content=entry.content)
            else:
                self.redirect("/" + entry_id +
                              "?error=You can't edit someone else's entry")
        else:
            self.redirect("/login?error=You must be logged in first")

    def post(self, entry_id):
        if not self.user:
            self.redirect('/')

        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            key = db.Key.from_path('Entry', int(entry_id), parent=blog_key())
            entry = db.get(key)
            entry.subject = subject
            entry.content = content
            entry.put()
            self.redirect('/' + entry_id)
        else:
            error = "subject and content, please!"
            self.render("editentry.html", subject=subject,
                        content=content, error=error)
