# import re
# import hmac
import os
import jinja2
import webapp2
from google.appengine.ext import db
from models import Comment, Entry, User, Like
from handlers import (BlogHandler, BlogFront, EntryPage, NewEntry, DeleteEntry, EditEntry, DeleteComment, EditComment, Signup, Login, Logout)


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

# TODO editentry doesn't put the original text in
# editcomment works fine though



# Help to render text

#in bloghandler
# def render_str(template, **params):
#     t = jinja_env.get_template(template)
#     return t.render(params)


# Aid in security and hashing
# def make_secure_val(val):
#     return '%s|%s' % (val, hmac.new(secret, val).hexdigest())

# def check_secure_val(secure_val):
#     val = secure_val.split('|')[0]
#     if secure_val == make_secure_val(val):
#         return val


# in entrypage
# def blog_key(name='default'):
#     return db.Key.from_path('blogs', name)

# # Validation of information
# USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
# EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
# PASS_RE = re.compile(r"^.{3,20}$")
#
# def valid_username(username):
#     return username and USER_RE.match(username)
#
# def valid_password(password):
#     return password and PASS_RE.match(password)
#
# def valid_email(email):
#     return not email or EMAIL_RE.match(email)

#
# class BlogHandler(webapp2.RequestHandler):
#     """
#     Handles common functions needed for the blog
#     """
#     def write(self, *a, **kw):
#         self.response.out.write(*a, **kw)
#
#     def render_str(self, template, **params):
#         params['user'] = self.user
#         return render_str(template, **params)
#
#     def render(self, template, **kw):
#         self.write(self.render_str(template, **kw))
#
#     def set_secure_cookie(self, name, val):
#         cookie_val = make_secure_val(val)
#         self.response.headers.add_header(
#             'Set-Cookie',
#             '%s=%s; Path=/' % (name, cookie_val))
#
#     def read_secure_cookie(self, name):
#         cookie_val = self.request.cookies.get(name)
#         return cookie_val and check_secure_val(cookie_val)
#
#     def set_login_cookie(self, user):
#         self.set_secure_cookie('user_id', str(user.key().id()))
#
#     def set_logout_cookie(self):
#         self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')
#
#     def initialize(self, *a, **kw):
#         webapp2.RequestHandler.initialize(self, *a, **kw)
#         uid = self.read_secure_cookie('user_id')
#         self.user = uid and User.by_id(int(uid))


#
# class BlogFront(BlogHandler):
#     """Front page of the blog"""
#     def get(self):
#         deleted_entry_id = self.request.get('deleted_entry_id')
#         entries = greetings = Entry.all().order('-created')
#         self.render('front.html', entries=entries, deleted_entry_id=deleted_entry_id)

# class EntryPage(BlogHandler):
#     """Page of an individual blog entry"""
#     def get(self, entry_id):
#
#         key = db.Key.from_path('Entry', int(entry_id), parent=blog_key())
#         entry = db.get(key)
#         comments = db.GqlQuery("select * from Comment where entry_id = " +
#                                entry_id + " order by created desc")
#         likes = db.GqlQuery("select * from Like where entry_id="+entry_id)
#
#         if not entry:
#             self.error(404)
#             return
#
#         error = self.request.get('error')
#
#         self.render("permalink.html", entry=entry, numlikes=likes.count(),
#                     comments=comments, error=error)
#
#     def post(self, entry_id):
#         key = db.Key.from_path('Entry', int(entry_id), parent=blog_key())
#         entry = db.get(key)
#
#         if not entry:
#             self.error(404)
#             return
#
#         if self.user :
#             #Check if a user clicked a "Like" button
#             if self.request.get('like') == "yes" :
#                 likes = db.GqlQuery("select * from Like where entry_id = " +
#                                     entry_id + " and user_id = " +
#                                     str(self.user.key().id()))
#
#                 if self.user.key().id() == entry.user_id:
#                     self.redirect("/" + entry_id +
#                                   "?error=You cannot like your own entry")
#
#                 elif likes.count() == 0:
#                     l = Like(parent=blog_key(), user_id=self.user.key().id(),
#                              entry_id=int(entry_id))
#                     l.put()
#             if self.request.get('like') == "no":
#                 likes = db.GqlQuery("select * from Like where entry_id = " +
#                                     entry_id + " and user_id = " +
#                                     str(self.user.key().id()))
#                 for l in likes:
#                     l.delete()
#
#             # Check if a user clicked the Comment button
#             if self.request.get('comment'):
#                 c = Comment(parent=blog_key(), user_id=self.user.key().id(),
#                             entry_id=int(entry_id),
#                             comment=self.request.get('comment'))
#                 c.put()
#         else:
#             self.redirect("/login?error=You must be logged in first")
#
#         comments = db.GqlQuery("select * from Comment where entry_id = " +
#                                entry_id + "order by created desc")
#         likes = db.GqlQuery("select * from Like where entry_id="+entry_id)
#         self.render("permalink.html", entry=entry,
#                     comments=comments, numlikes=likes.count())

# class NewEntry(BlogHandler):
#     """Page for writing a new blog entry"""
#     def get(self):
#         if self.user:
#             self.render("newentry.html")
#         else:
#             self.redirect("/login")
#
#     def post(self):
#         if not self.user:
#             self.redirect('/')
#
#         subject = self.request.get('subject')
#         content = self.request.get('content')
#
#         if subject and content:
#             p = Entry(parent=blog_key(), user_id=self.user.key().id(),
#                      subject=subject, content=content)
#             p.put()
#             self.redirect('/' + str(p.key().id()))
#         else:
#             error = "subject and content, please!"
#             self.render("newentry.html", subject=subject,
#                         content=content, error=error)


# class DeleteEntry(BlogHandler):
#     """Page for deleting a blog entry"""
#     def get(self, entry_id):
#         if self.user:
#             key = db.Key.from_path('Entry', int(entry_id), parent=blog_key())
#             entry = db.get(key)
#             if entry.user_id == self.user.key().id():
#                 entry.delete()
#                 self.redirect("/?deleted_entry_id="+entry_id)
#             else:
#                 self.redirect("/" + entry_id +
#                               "?error=You can't delete someone else's entry")
#         else:
#             self.redirect("/login?error=You must be logged in first")
#
# class EditEntry(BlogHandler):
#     """Page for editing a blog entry"""
#     def get(self, entry_id):
#         if self.user:
#             key = db.Key.from_path('Entry', int(entry_id), parent=blog_key())
#             entry = db.get(key)
#             if entry.user_id == self.user.key().id():
#                 self.render("editentry.html", subject=entry.subject,
#                             content=entry.content)
#             else:
#                 self.redirect("/" + entry_id +
#                               "?error=You can't edit someone else's entry")
#         else:
#             self.redirect("/login?error=You must be logged in first")
#
#     def post(self, entry_id):
#         if not self.user:
#             self.redirect('/')
#
#         subject = self.request.get('subject')
#         content = self.request.get('content')
#
#         if subject and content:
#             key = db.Key.from_path('Entry', int(entry_id), parent=blog_key())
#             entry = db.get(key)
#             entry.subject = subject
#             entry.content = content
#             entry.put()
#             self.redirect('/' + entry_id)
#         else:
#             error = "subject and content, please!"
#             self.render("editentry.html", subject=subject,
#                         content=content, error=error)

#
# class DeleteComment(BlogHandler):
#     """Page for deleting a comment"""
#     def get(self, entry_id, comment_id):
#         if self.user:
#             key = db.Key.from_path('Comment', int(comment_id),
#                                     parent=blog_key())
#             c = db.get(key)
#             if c.user_id == self.user.key().id():
#                 c.delete()
#                 self.redirect("/"+entry_id+"?deleted_comment_id=" +
#                               comment_id)
#             else:
#                 self.redirect("/" + entry_id +
#                               "?error=You can't delete someone else's comment")
#         else:
#             self.redirect("/login?error=You must be logged in first")

#
# class EditComment(BlogHandler):
#     """Page for editing a comment"""
#     def get(self, entry_id, comment_id):
#         if self.user:
#             key = db.Key.from_path('Comment', int(comment_id),
#                                    parent=blog_key())
#             c = db.get(key)
#             if c.user_id == self.user.key().id():
#                 self.render("editcomment.html", comment=c.comment)
#             else:
#                 self.redirect("/" + entry_id +
#                               "?error=You can't edit someone else's comment")
#         else:
#             self.redirect("/login?error=You must be logged in first")
#
#     def post(self, entry_id, comment_id):
#         if not self.user:
#             self.redirect('/')
#
#         comment = self.request.get('comment')
#         if comment:
#             key = db.Key.from_path('Comment',
#                                    int(comment_id), parent=blog_key())
#             c = db.get(key)
#             c.comment = comment
#             c.put()
#             self.redirect('/' + entry_id)
#         else:
#             error = "You need to write something"
#             self.render("editentry.html", subject=subject,
#                         content=content, error=error)

# class Signup(BlogHandler):
#     """Page for creating a user account"""
#     def get(self):
#         self.render("signup.html")
#
#     def post(self):
#         have_error = False
#         self.username = self.request.get('username')
#         self.password = self.request.get('password')
#         self.verify = self.request.get('verify')
#         self.email = self.request.get('email')
#
#         params = dict(username=self.username,
#                       email=self.email)
#
#         if not valid_username(self.username):
#             params['error_username'] = "Invalid username."
#             have_error = True
#
#         if not valid_password(self.password):
#             params['error_password'] = "Invalid password."
#             have_error = True
#         elif self.password != self.verify:
#             params['error_verify'] = "Your passwords didn't match."
#             have_error = True
#
#         if not valid_email(self.email):
#             params['error_email'] = "Invalid email."
#             have_error = True
#
#         if have_error:
#             self.render('signup.html', **params)
#         else:
#             self.done()
#
#     def done(self, *a, **kw):
#         u = User.by_name(self.username)
#         if u:
#             msg = 'This user already exists'
#             self.render('signup.html', error_username=msg)
#         else:
#             u = User.register(self.username, self.password, self.email)
#             u.put()
#
#             self.set_login_cookie(u)
#             self.redirect('/')
#
# class Login(BlogHandler):
#     """Page for logging into a user account"""
#     def get(self):
#         self.render('login.html', error=self.request.get('error'))
#
#     def post(self):
#         username = self.request.get('username')
#         password = self.request.get('password')
#
#         u = User.login(username, password)
#         if u:
#             self.set_login_cookie(u)
#             self.redirect('/')
#         else:
#             msg = 'Invalid login'
#             self.render('login.html', error=msg)

#
# class Logout(BlogHandler):
#     """Page for logging out of a user account"""
#     def get(self):
#         self.set_logout_cookie()
#         self.redirect('/')

app = webapp2.WSGIApplication([
                               ('/?', BlogFront),
                               ('/([0-9]+)', EntryPage),
                               ('/newentry', NewEntry),
                               ('/deleteentry/([0-9]+)', DeleteEntry),
                               ('/editentry/([0-9]+)', EditEntry),
                               ('/deletecomment/([0-9]+)/([0-9]+)',
                                DeleteComment),
                               ('/editcomment/([0-9]+)/([0-9]+)',
                                EditComment),
                               ('/signup', Signup),
                               ('/login', Login),
                               ('/logout', Logout),
                               ],
                              debug=True)
