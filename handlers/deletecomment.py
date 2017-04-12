
from google.appengine.ext import db

from bloghandler import BlogHandler
from models import User
from models import Entry
from models import Comment

def blog_key(name='default'):
    return db.Key.from_path('blogs', name)

class DeleteComment(BlogHandler):
    """Page for deleting a comment"""
    def get(self, entry_id, comment_id):
        if self.user:
            key = db.Key.from_path('Comment', int(comment_id),
                                    parent=blog_key())
            c = db.get(key)
            if c.user_id == self.user.key().id():
                c.delete()
                self.redirect("/"+entry_id+"?deleted_comment_id=" +
                              comment_id)
            else:
                self.redirect("/" + entry_id +
                              "?error=You can't delete someone else's comment")
        else:
            self.redirect("/login?error=You must be logged in first")
