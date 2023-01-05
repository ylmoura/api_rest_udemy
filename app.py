from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST
from db.config import config
from router import routes

app = Flask(__name__)
config(app)
api = Api(app)
jwt = JWTManager(app)

# antes da primeira requisição eercutar funcao abaixo
@app.before_first_request
def cria_banco():
    banco.create_all()

@jwt.token_in_blocklist_loader
def verifica_blacklist(self,token):
    return token['jti'] in BLACKLIST

@jwt.revoked_token_loader
def token_de_acesso_invalidado(self,token):
            jwtkn = token['jti']
            return jsonify({'message': 'token {} already been revoked!'.format(jwtkn)}), 401 # unauthorized
routes(api)

if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)



#- Substitua @jwt_required por ===> @jwt_required()

#- Renomeie @jwt.token_in_blacklist_loader para ===>  @jwt.token_in_blocklist_loader

#- Substitua get_raw_jwt por ===> get_jwt