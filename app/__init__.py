from flask import Flask
from app.routes import api_create 

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api_create )
    return app


