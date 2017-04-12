from google.appengine.ext import db

from user import User


class Like(db.Model):
    user_id = db.IntegerProperty(required=True)
    entry_id = db.IntegerProperty(required=True)

    def getUserName(self):
        user = User.by_id(self.user_id)
        return user.name
