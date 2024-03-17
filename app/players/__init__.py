from flask import Blueprint

bp = Blueprint('players', __name__)

from app.players import routes