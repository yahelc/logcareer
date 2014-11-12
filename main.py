#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#	 http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from google.appengine.api import mail
from google.appengine.ext.webapp import template
import jinja2
import os
from google.appengine.api import users
from models.subscriber import Subscriber
from models.mailing import Mailing
from models.entry import Entry
from google.appengine.ext import db
from datetime import datetime
from datetime import timedelta
import json
import logging

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + "/templates"),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class OutboundEmailHandler(webapp2.RequestHandler):
	def get(self):
		target = Subscriber.all().filter("next_email_dt < ", datetime.now()).get()
		if target is None:
			self.response.write("None")
			return
		mail.send_mail(sender="logcareer.com Update <update@logcareer.com>",
					  to="%s <%s>"% (target.user.nickname(), target.user.email() ),
					  subject="You've signed up for LogCareer",
					  body="""##- Please type your reply above this line -##
					
		Dear %s:

		Reply to this email. 

		The logcareer.com Team
		"""%(target.user.nickname()))
		
		target.next_email_dt = target.next_email_dt + timedelta(days=target.days_between_emails)
		target.put()
		Mailing(email=target.email).put()
		self.response.write(target.email)
		

class MainHandler(webapp2.RequestHandler):
	def get(self):
		greetings = "Welcome."
		name = False
		user_id = False
		email = False
		entries = False
		title ="Hi!"

		if users.get_current_user():
			user =  users.get_current_user()
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
			name = user.nickname()
			user_id = user.user_id()
			email = user.email()
			subscriber = Subscriber.get_or_insert(email, email=email)
			entries_db = db.Query(Entry)
			entries = []
			entries_db = entries_db.filter('email =', email).fetch(1000)
			for entry in entries_db:
				entries.append({"body":entry.body, "created": entry.created})
			
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'
		logging.info("ENTRIES:")
		logging.info(entries)
		template_values = {
		'greetings': greetings,
		'url': url,
		'url_linktext': url_linktext,
		'name' : name,
		'user_id': user_id,
		'email': email,
		'subscriber': db.to_dict(subscriber),
		'entries': entries
		}
		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.out.write(template.render(template_values))


app = webapp2.WSGIApplication([
('/outgoing', OutboundEmailHandler),
('/', MainHandler)
], debug=True)
