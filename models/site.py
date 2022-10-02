
from sql_alchemy import banco
from models.hotel import * 


class SiteModel(banco.Model):
    __tablename__=  'sites'

    site_id = banco.Column(banco.Integer, primary_key=True)
    url = banco.Column(banco.String(80))
    hoteis = banco.relationship('HotelModel')  # lista de objetos hoteis
    

    def __init__(self, url):
        self.url = url

    def json(self):
        return {
            'site_id': self.site_id,
            'url': self.url,
            'hoteis': [hoteis.json() for hoteis in self.hoteis]
        }
    @classmethod   #não precisa passar parametro apenas retorna
    def find_url(cls, url):
        site = cls.query.filter_by(url = url).first() #quando escreve cls e como tivesse acesando a class UrlModel
        if site:
            return site
        return None
    
    def save_site(self):
        banco.session.add(self) #adicionar os argumentos no banco e salva
        banco.session.commit()

    def delete_site(self):
        #deletando todos hoteis relacionados ao site
        [hotel.delete_hotel() for hotel in self.hoteis]

        #deletando site
        banco.session.delete(self)
        banco.session.commit()