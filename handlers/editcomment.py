from functools import wraps
from google.appengine.ext import db

from bloghandler import (BlogHandler, comment_exists, user_owns_comment,
                          user_logged_in, blog_key)
from models import Comment

class EditComment(BlogHandler):
    """Page for editing a comment"""
    @user_logged_in
    @comment_exists
    @user_owns_comment
    def get(self, entry_id, comment_id):
        key = db.Key.from_path('Comment', int(comment_id),
                               parent=blog_key())
        c = db.get(key)
        self.render("editcomment.html", comment=c.comment)

    @user_logged_in
    @comment_exists
    @user_owns_comment
    def post(self, entry_id, comment_id):
        submitted = self.request.get('submitted')
        if submitted =='no':
            self.redirect('/' + entry_id)

        comment = self.request.get('comment')
        if comment:
            key = db.Key.from_path('Comment',
                                   int(comment_id), parent=blog_key())
            c = db.get(key)
            c.comment = comment
            c.put()
            self.redirect('/' + entry_id)
        else:
            error = "You need to write something"
            self.render("editentry.html", subject=subject,
                        content=content, error=error)
