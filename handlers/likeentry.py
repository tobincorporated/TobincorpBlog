from functools import wraps
from google.appengine.ext import db

from bloghandler import (BlogHandler, entry_exists, user_logged_in,
                          user_owns_entry, blog_key)
from models import User, Entry, Like, Comment



class EntryPage(BlogHandler):
