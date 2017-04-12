import webapp2
from handlers import (BlogHandler, BlogFront, EntryPage, NewEntry, DeleteEntry,
                      EditEntry, DeleteComment, EditComment, Signup, Login,
                      LikeEntry, Logout)

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
                               ('/likeentry/([0-9]+)', LikeEntry ),
                               ],
                              debug=True)
