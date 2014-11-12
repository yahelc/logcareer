from google.appengine.ext import db

class Subscriber(db.Model):
  email = db.EmailProperty()
  user = db.UserProperty(auto_current_user_add=True)
  is_subscribed = db.BooleanProperty(default=True)
  created = db.DateTimeProperty(auto_now_add=True)
  next_email_dt = db.DateTimeProperty(auto_now_add=True)
  days_between_emails = db.IntegerProperty(default=7)