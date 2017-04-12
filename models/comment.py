from google.appengine.ext import db

from user import User

class Comment(db.Model):
    """Stores information on each comment in the blog
    Attributes:
        user_id: ID number of the liking user
        entry_id: ID number of the entry liked
        comment: Text of the comment itself
        created: Datetime the comment was created
        last_modified: Datetime the comment was last modified
    """
    user_id = db.IntegerProperty(required=True)
    entry_id = db.IntegerProperty(required=True)
    comment = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)

    def getUserName(self):
        user = User.by_id(self.user_id)
        return user.name
