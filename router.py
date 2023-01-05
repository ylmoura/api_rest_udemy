from resources.hotel import Hoteis, Hotel
from resources.usuario import User, UserRegister, UserLogin, UserLogout
from resources.site import Sites, Site


def routes(api):
    api.add_resource(Hoteis, '/hoteis')
    api.add_resource(Hotel, '/hoteis/<string:hotel_id>')
    api.add_resource(User, '/usuarios/<int:user_id>')
    api.add_resource(UserRegister, '/cadastro')
    api.add_resource(UserLogin, '/login')
    api.add_resource(UserLogout, '/logout')
    api.add_resource(Sites, '/sites')
    api.add_resource(Site, '/sites/<string:url>')