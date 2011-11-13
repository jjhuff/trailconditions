from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import datastore

class Admin(webapp.RequestHandler):
    def get(self):
        areas = []
        for area in datastore.Area.all():
            areas.append({
                'key': area.key(),
                'name': area.name
                })
        template_values={
                'areas': areas
                }
        self.response.out.write(template.render('templates/admin.html', template_values))

    def post(self):
        action = self.request.get('action')
        if action == 'Add Area':
            area = datastore.Area(name=self.request.get('area_name'))
            area.map_url = self.request.get('area_map_url')
            area.put()
        elif action == 'Add Trail':
            trail = datastore.Trail(
                    area = datastore.Area.get(self.request.get('trail_area_id')),
                    name = self.request.get('trail_name'))
            trail.put()
        self.get()
