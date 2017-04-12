from google.appengine.ext import db

from user import User

class Like(db.Model):
    """Stores information on each 'like' in the blog
    Attributes:
        user_id: ID number of the liking user
        entry_id: ID number of the entry liked
    """
    user_id = db.IntegerProperty(required=True)
    entry_id = db.IntegerProperty(required=True)

    def getUserName(self):
        user = User.by_id(self.user_id)
        return user.name
