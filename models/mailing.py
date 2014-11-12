from google.appengine.ext import db

class Mailing(db.Model):
  email = db.EmailProperty()
  created = db.DateTimeProperty(auto_now_add=True)
