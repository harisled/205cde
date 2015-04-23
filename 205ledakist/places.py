#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import jinja2
import webapp2

import upload

from google.appengine.api import users
from google.appengine.ext import ndb

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'templates')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Author(ndb.Model): #code taken from lab examples
    """Sub model for representing an author."""
    identity = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)

class Place(ndb.Model): #code manipulated from lab examples
    """model for the place entries"""
    author = ndb.StructuredProperty(Author)
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)

class placesmain(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
        template = JINJA_ENVIRONMENT.get_template('places.html')
        self.response.write(template.render())

class places(webapp2.RequestHandler):
    def get(self):
        # template = JINJA_ENVIRONMENT.get_template('history.html')
        # self.response.write(template.render())
        self.response.write('eleos')

app = webapp2.WSGIApplication([
    (r'/places/?', placesmain),
    (r'/place/(.*)', places),
    ('/up', upload.PhotoUploadFormHandler),
    ('/upload_photo', upload.PhotoUploadHandler)

], debug=True)
