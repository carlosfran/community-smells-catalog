from flask import Flask
from flask_babel import Babel
from config import Config

app = Flask(__name__)

app.config.from_object(Config)
app.app_context()

babel = Babel(app)

from app import routes