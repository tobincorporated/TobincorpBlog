from functools import wraps
from google.appengine.ext import db

from bloghandler import (BlogHandler, entry_exists, user_logged_in, blog_key)
from models import User, Entry, Like



class LikeEntry(BlogHandler):
    @user_logged_in
    @entry_exists
    def get(self, entry_id):
        key = db.Key.from_path('Entry', int(entry_id), parent=blog_key())
        entry = db.get(key)
        if self.request.get('like') == "yes" :
            likes = db.GqlQuery("select * from Like where entry_id = " +
                                entry_id + " and user_id = " +
                                str(self.user.key().id()))

            if self.user.key().id() == entry.user_id:
                self.redirect("/" + entry_id +
                              "?error=You cannot like your own entry")

            elif likes.count() == 0:
                l = Like(parent=blog_key(), user_id=self.user.key().id(),
                         entry_id=int(entry_id))
                l.put()
        if self.request.get('like') == "no":
            likes = db.GqlQuery("select * from Like where entry_id = " +
                                entry_id + " and user_id = " +
                                str(self.user.key().id()))
            for l in likes:
                l.delete()
        self.redirect('/'+entry_id)
