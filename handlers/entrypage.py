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

        error = self.request.get('error')
        self.render("permalink.html", entry=entry, numlikes=likes.count(),
                    comments=comments, error=error)

    @entry_exists
    @user_logged_in
    def post(self, entry_id):
        key = db.Key.from_path('Entry', int(entry_id), parent=blog_key())
        entry = db.get(key)

        # Check if a user clicked the Comment button
        if self.request.get('comment'):
            c = Comment(parent=blog_key(), user_id=self.user.key().id(),
                        entry_id=int(entry_id),
                        comment=self.request.get('comment'))
            c.put()

        comments = db.GqlQuery("select * from Comment where entry_id = " +
                               entry_id + "order by created desc")
        likes = db.GqlQuery("select * from Like where entry_id="+entry_id)
        self.redirect('/'+entry_id)
