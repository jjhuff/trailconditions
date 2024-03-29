#!/usr/bin/env python
#
# Copyright 2011 Justin Huff <jjhuff@mspin.net>
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

from google.appengine.dist import use_library
use_library('django', '1.2')

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

import admin
import datastore

class MainPage(webapp.RequestHandler):
    def get(self):
        template_values={
                'areas': datastore.Area.all(),
                'stars': range(0,5)
                }
        self.response.out.write(template.render('templates/index.html', template_values))

class AddRating(webapp.RequestHandler):
    def post(self):
        trail = datastore.Trail.get(self.request.get('trail_id'))
        rating = datastore.Rating(
                trail = trail,
                rating = int(self.request.get('trail_rating')))
        rating.put()
        self.response.out.write(rating.key())

        # Update the ratings
        datastore.UpdateRatings(trail)

class UpdateRatings(webapp.RequestHandler):
    def get(self):
        for trail in datastore.Trail.all():
            datastore.UpdateRatings(trail)

class Ratings(webapp.RequestHandler):
    def get(self):
        trail = datastore.Trail.get(self.request.get('trail_id'))
        template_values={
                'trail': trail,
                'ratings': trail.rating_set.order('-timestamp'),
                'stars': range(0,5)
                }
        self.response.out.write(template.render('templates/ratings.html', template_values))


application = webapp.WSGIApplication([
        ('/', MainPage),
        ('/admin', admin.Admin),
        ('/addrating', AddRating),
        ('/updateratings', UpdateRatings),
        ('/ratings', Ratings),
    ],debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
