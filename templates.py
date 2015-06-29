import os
import jinja2
import webapp2

from google.appengine.ext import ndb

#to initialize jinja
#directory that my current file is in os.path.dirname(__file__)
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader (template_dir),
  autoescape = True)

class Message(ndb.Model):
  comment = ndb.StringProperty()
  date = ndb.DateTimeProperty(auto_now_add=True)

class Handler(webapp2.RequestHandler):
  def write(self, *a, **kw):
    self.response.out.write(*a, **kw)

  def render_str(self, template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

  def render(self, template, **kw):
    self.write(self.render_str(template, **kw))



class MainPage(Handler):
  def get(self):
    # error = self.request.get('error','') 
     
    query = Message.query().order(Message.date)
    message_list = query.fetch()

    self.render("form.html", message_list=message_list)
    message = message_list
    # self.response.out.write(message)

  def post(self):
    # date = self.request.get('date')
    comment = self.request.get('comment')

    # if either of the fields (link or comment) is blank
    if comment:
        message = Message(comment=comment)
        message.put()
        import time
        time.sleep(.1)
        self.redirect('/')
        self.response.out.write(message)
    else:
      self.response.out.write('Please leave a comment!') 

app = webapp2.WSGIApplication([('/', MainPage),
], debug=True)
