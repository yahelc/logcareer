from google.appengine.ext import db

class Entry(db.Model):
  email = db.EmailProperty()
  created = db.DateTimeProperty(auto_now_add=True)
  body = db.TextProperty()