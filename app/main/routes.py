from app import db
from flask import render_template, redirect, url_for
import sqlalchemy as sa
from app.models import TarotGame, Player

from app.main import bp


@bp.route('/')
@bp.route('/index')
def index():
    return redirect(url_for('main.games'))

@bp.route('/games', methods=['POST', 'GET'])
def games():
    tarot_games = db.session.scalars(sa.select(TarotGame).order_by(TarotGame.creation_date.desc())).all()
    players_username = [[player.username for player in db.session.scalars(game.players.select()).all()] for game in tarot_games]
    
    return render_template('main/games.html', tarot_games=tarot_games, players_username=players_username, title="Parties")

@bp.route('/players')
def players():
    p = db.session.scalars(sa.select(Player)).all()
    return render_template("main/players.html", players=p, title="Joueurs")