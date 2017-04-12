
from google.appengine.ext import db
import os
import jinja2
from user import User
template_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ),
                                '..', 'templates'))
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)




def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class Entry(db.Model):
    """Stores information on each blog entry
    Attributes:
        user_id: ID number of the entry's author
        subject: subject line of the entry
        content: text of the blog entry
        create: datetime when the entry was created
        last_modified: datetime when the entry was last modified
        """
    user_id = db.IntegerProperty(required=True)
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)

    def getUserName(self):
        user = User.by_id(self.user_id)
        return user.name

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("entry.html", p = self,
        entry_id = str(self.key().id()))
