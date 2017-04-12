from functools import wraps
from google.appengine.ext import db

from bloghandler import (BlogHandler, entry_exists, user_logged_in,
                          user_owns_entry, blog_key)
from models import User, Entry, Like, Comment

class EntryPage(BlogHandler):
    """Page of an individual blog entry"""
    @entry_exists
    def get(self, entry_id):

        key = db.Key.from_path('Entry', int(entry_id), parent=blog_key())
        entry = db.get(key)
        comments = db.GqlQuery("select * from Comment where entry_id = " +
                               entry_id + " order by created desc")
        likes = db.GqlQuery("select * from Like where entry_id="+entry_id)

        if not entry:
            self.error(404)
            return

        error = self.request.get('error')
        self.render("permalink.html", entry=entry, numlikes=likes.count(),
                    comments=comments, error=error)

    @entry_exists
    @user_logged_in
    def post(self, entry_id):
        key = db.Key.from_path('Entry', int(entry_id), parent=blog_key())
        entry = db.get(key)

        #Check if a user clicked a "Like" button
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

        # Check if a user clicked the Comment button
        if self.request.get('comment'):
            c = Comment(parent=blog_key(), user_id=self.user.key().id(),
                        entry_id=int(entry_id),
                        comment=self.request.get('comment'))
            c.put()

        comments = db.GqlQuery("select * from Comment where entry_id = " +
                               entry_id + "order by created desc")
        likes = db.GqlQuery("select * from Like where entry_id="+entry_id)
        self.render("permalink.html", entry=entry,
                    comments=comments, numlikes=likes.count())
