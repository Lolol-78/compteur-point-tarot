from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_colorpicker import colorpicker
from flask_moment import Moment
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)
bootstrap = Bootstrap(app)
color_picker = colorpicker(app)
moment = Moment(app)

from app import routes, models