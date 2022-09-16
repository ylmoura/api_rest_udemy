from flask_restful import Resource, reqparse
from models.hotel import *
from flask_jwt_extended import jwt_required

class Hoteis(Resource):
    def get(self):
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}

class Hotel(Resource):

    atributo = reqparse.RequestParser()
    atributo.add_argument('nome', type= str, required=True, help="The field 'name' cannot be left blank")
    atributo.add_argument('estrelas', type= float, required=True, help="The field 'estrelas' cannot be left blank")
    atributo.add_argument('diaria')
    atributo.add_argument('cidade')

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel not found.'}, 404 # not found

    def post(self,hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {'message': "Hotel id '{}' already exists.".format(hotel_id)}, 400 # bad requests
        dados = Hotel.atributo.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'message': 'An error occurred while saving the hotel'}, 500
        return hotel.json()
        

    def put(self,hotel_id):
        dados = Hotel.atributo.parse_args()
        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            try:
                hotel_encontrado.save_hotel()
            except:
                return {'message': 'An error occurred while saving the hotel'}, 500
            return hotel_encontrado.json(), 200
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'message': 'An error occurred while saving the hotel'}, 500
        return hotel.json(), 201 # create a new hotel_id

    def delete(self,hotel_id):
        #global hoteis # dizendo que a variavel hoteis já  existe para eu poder fazer referencia novamente  
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message': 'An error occurred while deleting the hotel'}
            return{'message':'Hotel deleted successfully'}
        return {'message': 'Hotel not found.'},404