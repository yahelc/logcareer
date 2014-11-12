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
import logging
import webapp2
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
from models.entry import Entry
import re
from email.utils import parseaddr
from email_reply_parser import EmailReplyParser


class LogSenderHandler(InboundMailHandler):
	def receive(self, mail_message):
		logging.info("Received a message from: " + mail_message.sender)
		logging.info("Subject: " + mail_message.subject)
		logging.info("Sender:" + mail_message.sender)
		bodies = mail_message.bodies("text/plain")
		email = parseaddr(mail_message.sender)[1]
		for content_type, body in bodies:
			reply = EmailReplyParser.parse_reply(body.decode())
			Entry(email=email, body=reply ).put()
			logging.info("PUT: " + reply )
			logging.info("email: " + email)
			
		logging.info(mail_message.original)


app = webapp2.WSGIApplication([LogSenderHandler.mapping()], debug=True)
