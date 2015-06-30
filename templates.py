import os
import jinja2
import webapp2

from google.appengine.ext import ndb

#to initialize jinja
#directory that my current file is in os.path.dirname(__file__)
template_dir = os.path.join(os.path.dirname('index_Stage4.html'), 'templates')
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
    error = self.request.get('error','') 
    comment = self.request.get_all('comment') 

    #Create key
    comment_key = ndb.Key('MainPage','message_page')

    message_page = Message(comment='')
    message_query = Message.query(ancestor=comment_key).order(Message.date)

    query=Message.query().order(Message.date)
    message_list = query.fetch()

    self.render("form.html", comment=message_list, error=error)
  
 
  def post(self):

    pull_posts=5
    query=Message.query()
    page_comments = query.fetch(pull_posts)

    
    comment = self.request.get('comment')
    #
 

    # if either of the fields (link or comment) is blank
    if comment:
        message_page = Message(comment=comment)
        message_page.content = self.request.get('comment')
        message_page.put()
        import time
        time.sleep(.1)
        self.redirect('/')        
    else:
      self.redirect('/?error=Please leave a comment!') 

app = webapp2.WSGIApplication([('/', MainPage),
], debug=True)
