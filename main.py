import os
import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Blog(db.Model):
    title = db.StringProperty(required = True)
    blog_post = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)


class MainPage(Handler):
    def render_front(self, title="", blog_post="", error=""):
        posts = db.GqlQuery("SELECT * FROM Blog "
                          "ORDER BY created DESC ")
        self.render("front.html", title=title, blog_post=blog_post, error=error, posts=posts)

    def get(self):
        self.render_front()

    def post(self):
        title = self.request.get("title")
        blog_post = self.request.get("blog_post")

        if title and blog_post:
            a = Blog(title = title, blog_post = blog_post)
            a.put()
            self.redirect("/")
        else:
            error = "Hey! We need both a title and some dam blog content sucka!"
            self.render_front(title, blog_post, error)



app = webapp2.WSGIApplication([('/', MainPage,
                                '/blog', Blog
                                )], debug=True)
