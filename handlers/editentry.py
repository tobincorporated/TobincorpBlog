
from google.appengine.ext import db
from bloghandler import (BlogHandler, entry_exists, user_logged_in,
                         user_owns_entry, blog_key)
from models import Entry

class EditEntry(BlogHandler):
    """Handler for editing a blog entry"""
    @user_logged_in
    @entry_exists
    @user_owns_entry
    def get(self, entry_id):
        key = db.Key.from_path('Entry', int(entry_id), parent=blog_key())
        entry = db.get(key)
        self.render("editentry.html", subject=entry.subject,
                        content=entry.content)

    @user_logged_in
    @entry_exists
    @user_owns_entry
    def post(self, entry_id):
        submitted = self.request.get('submitted')

        subject = self.request.get('subject')
        content = self.request.get('content')
        if submitted =='yes':
            if subject and content:
                key = db.Key.from_path('Entry', int(entry_id), parent=blog_key())
                entry = db.get(key)
                entry.subject = subject
                entry.content = content
                entry.put()
                self.redirect('/' + entry_id)
            else:
                error = "subject and content, please!"
                self.render("editentry.html", subject=subject,
                            content=content, error=error)
        else:
            self.redirect('/' + entry_id)
