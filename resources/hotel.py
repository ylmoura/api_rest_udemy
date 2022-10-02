from xml.etree.ElementInclude import LimitedRecursiveIncludeError
from flask_restful import Resource, reqparse
from models.hotel import *
from flask_jwt_extended import jwt_required
import sqlite3
from resources.filtros import *


path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type= str)
path_params.add_argument('estrelas_min', type= float)
path_params.add_argument('estrelas_max', type= float)
path_params.add_argument('diaria_min', type= float)
path_params.add_argument('diaria_max', type= float)
path_params.add_argument('limit', type= float)
path_params.add_argument('offset', type= float)


# path /hoteis?cidade= Rio de Janeiro&estrelas_min=4&diaria_max=400
class Hoteis(Resource):
    def get(self):
        connection = sqlite3.connect('banco.db')
        cursor = connection.cursor()
        dados = path_params.parse_args()
        # Caso não passe o parametro o dado não será util
        dados_validos = {chave:dados[chave] for chave in dados if dados[chave] is not None}
        parametros = normalize_path_params(**dados_validos)
        
        if not parametros.get('cidade'): # não foi passado cidade no parametros
            tupla = tuple([parametros[chave] for chave in parametros]) # valores do where é passado na tuple
            resultado = cursor.execute(consulta_sem_cidade, tupla)
        else:
            consulta = consulta_com_cidade
            tupla = tuple([parametros[chave] for chave in parametros])
            resultado = cursor.execute(consulta, tupla)

        hoteis = []
        
        for linha in resultado:
            hoteis.append({
            'hotel_id': linha[0] ,
            'nome': linha[1],
            'estrelas': linha[2],
            'diaria': linha[3],
            'cidade': linha[4],
            'site_id': linha[5]
            })
        
        return {'hoteis': hoteis} # SELECT * FROM tb_hoteis


class Hotel(Resource):

    atributo = reqparse.RequestParser()
    atributo.add_argument('nome', type= str, required=True, help="The field 'name' cannot be left blank")
    atributo.add_argument('estrelas') #, type= float, required=True, help="The field 'estrelas' cannot be left blank")
    atributo.add_argument('diaria')
    atributo.add_argument('cidade')
    atributo.add_argument('site_id', type= int, required=True, help="The field 'site_id' cannot be left blank")

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel not found.'}, 404 # not found

    @jwt_required()
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
        
    @jwt_required()
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
    @jwt_required()
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