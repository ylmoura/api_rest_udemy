from flask_restful import Resource
from models.site import *

class Sites(Resource):
    def get(self):
        return {'site': [site.json() for site in SiteModel.query.all()]}

class Site(Resource):
    def get(self,url):
        site = SiteModel.find_url(url)

        if site:
            return site.json()
        return {'message': 'site not found'}, 404 # not found

    def post(self,url):
        if SiteModel.find_url(url):
            return {'message': "Site '{}' already exists.".format(url)}, 400 # bad requests
        site = SiteModel(url)
        try:
            site.save_site()
        except:
            return {'message': 'An error occurred while saving the site'}, 500
        return site.json()
    
    def delete(self,url):
        
        site = SiteModel.find_url(url)
        if site:
            try:
                site.delete_site()
            except:
                return {'message': 'An error occurred while deleting the site'}
            return{'message':'site deleted successfully'}
        return {'message': 'site not found.'},404