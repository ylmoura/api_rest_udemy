

def config(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db' #se precisar mudar o banco de dados só mudar a variavel
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'
    app.config['JWT_BLACKLIST_ENABLED'] = True