
from sql_alchemy import banco


class UserModel(banco.Model):
    __tablename__=  'tb_usuarios'

    user_id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.String(40))   
    senha = banco.Column(banco.String(40))

    def __init__(self, login, senha):
        self.login = login
        self.senha = senha

    def json(self):
        return {
            'user_id': self.user_id,
            'login': self.login
        }
    @classmethod   #não precisa passar parametro apenas retorna
    def find_user(cls, user_id):
        user = cls.query.filter_by(user_id = user_id).first() #quando escreve cls e como tivesse asscendo a class HotelModel
        if user:
            return user
        return None
    @classmethod 
    def find_by_login(cls, login):
        user = cls.query.filter_by(login = login).first() #quando escreve cls e como tivesse asscendo a class HotelModel
        if user:
            return user
        return None
    
    def save_user(self):
        banco.session.add(self) #adicionar os argumentos no banco e salva
        banco.session.commit()

    def delete_user(self):
        banco.session.delete(self)
        banco.session.commit()