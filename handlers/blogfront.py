from bloghandler import BlogHandler
from models import Entry



class BlogFront(BlogHandler):
    """Front page of the blog"""
    def get(self):
        deleted_entry_id = self.request.get('deleted_entry_id')
        entries = greetings = Entry.all().order('-created')
        self.render('front.html', entries=entries, deleted_entry_id=deleted_entry_id)
