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

import datetime
from google.appengine.ext import db

class Area(db.Model):
    name = db.StringProperty(required=True)
    map_url = db.StringProperty()

class Trail(db.Model):
    area = db.ReferenceProperty(Area, required=True)
    name = db.StringProperty(required=True)
    current_rating = db.FloatProperty()
    current_rating_count = db.IntegerProperty()

class Rating(db.Model):
    trail = db.ReferenceProperty(Trail, required=True)
    rating = db.IntegerProperty(required=True)
    timestamp = db.DateTimeProperty(auto_now=True, auto_now_add=True)

def UpdateRatings(trail):
    min_time = datetime.datetime.now() - datetime.timedelta(days=2)
    ratings = Rating.all().filter('trail =', trail.key()).filter('timestamp >', min_time)
    total=0
    count=0
    for rating in ratings:
        total += rating.rating
        count += 1
    if count > 0:
        trail.current_rating = round(float(total)/count)
    else:
        trail.current_rating = -1.0
    trail.current_rating_count = count
    trail.put()
