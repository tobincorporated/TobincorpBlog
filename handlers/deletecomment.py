
from google.appengine.ext import db
from bloghandler import (BlogHandler, comment_exists, user_owns_comment,
                         user_logged_in, blog_key)
from models import Comment

class DeleteComment(BlogHandler):
    """Handler for deleting a comment"""
    @user_logged_in
    @comment_exists
    @user_owns_comment
    def get(self, entry_id, comment_id):
        key = db.Key.from_path('Comment', int(comment_id), parent=blog_key())
        c = db.get(key)
        c.delete()
        self.redirect("/"+entry_id+"?deleted_comment_id=" + comment_id)
