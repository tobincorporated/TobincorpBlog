
from google.appengine.ext import db
from bloghandler import (BlogHandler, entry_exists, user_logged_in,
                          user_owns_entry, blog_key)
from models import Entry

class DeleteEntry(BlogHandler):
    """Handler for deleting a blog entry"""
    @user_logged_in
    @entry_exists
    @user_owns_entry
    def get(self, entry_id):
        key = db.Key.from_path('Entry', int(entry_id), parent=blog_key())
        entry = db.get(key)
        entry.delete()
        self.redirect("/?deleted_entry_id="+entry_id)
