
from google.appengine.ext import db
from bloghandler import BlogHandler
from models import Entry, User



def blog_key(name='default'):
    return db.Key.from_path('blogs', name)

class DeleteEntry(BlogHandler):
    """Handler for deleting a blog entry"""
    def get(self, entry_id):
        if self.user:
            key = db.Key.from_path('Entry', int(entry_id), parent=blog_key())
            entry = db.get(key)
            if entry.user_id == self.user.key().id():
                entry.delete()
                self.redirect("/?deleted_entry_id="+entry_id)
            else:
                self.redirect("/" + entry_id +
                              "?error=You can't delete someone else's entry")
        else:
            self.redirect("/login?error=You must be logged in first")
