
from google.appengine.ext import db

from bloghandler import BlogHandler
from models import User
from models import Entry
from models import Comment

def blog_key(name='default'):
    return db.Key.from_path('blogs', name)


class EditComment(BlogHandler):
    """Page for editing a comment"""
    def get(self, entry_id, comment_id):
        if self.user:
            key = db.Key.from_path('Comment', int(comment_id),
                                   parent=blog_key())
            c = db.get(key)
            if c.user_id == self.user.key().id():
                self.render("editcomment.html", comment=c.comment)
            else:
                self.redirect("/" + entry_id +
                              "?error=You can't edit someone else's comment")
        else:
            self.redirect("/login?error=You must be logged in first")

    def post(self, entry_id, comment_id):
        if not self.user:
            self.redirect('/')

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
