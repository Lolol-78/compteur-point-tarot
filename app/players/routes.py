from app import db
from flask import render_template, flash, redirect, url_for, request
import sqlalchemy as sa
from app.models import Player
from app.players.forms import NewPlayerForm, EditPlayerForm

from app.players import bp



@bp.route("/new_player", methods=["POST", "GET"])
def new_player():
    form = NewPlayerForm()
    if form.validate_on_submit():
        player = Player(username=form.username.data, gender=form.gender.data, color=request.form.get("color"))
        db.session.add(player)
        db.session.commit()
        flash(f"Le joueur {player.username} a bien été créé !")
        return redirect(url_for("players.new_player"))
    return render_template("players/new_player.html", form=form, title="Nouveau Joueur")

@bp.route('/players/<player_id>/get_edit')
def get_edit_player(player_id):
    player = db.session.get(Player, int(player_id))
    form = EditPlayerForm(username=player.username, gender=player.gender, color=player.color)
    return render_template("players/get_player.html", player=player, form=form)

@bp.route('/players/<int:player_id>/get_normal')
def get_normal_player(player_id):
    player = db.session.get(Player, player_id)
    if player is None:
        return None
    return render_template("players/get_player.html", player=player)

@bp.route('/players/<int:player_id>/edit', methods=["POST", "GET"])
def edit_player(player_id):
    player = db.session.get(Player, player_id)
    if player is None:
        return None
    form = EditPlayerForm(username=player.username, gender=player.gender, color=player.color)
    form.player = player
    if form.validate_on_submit():
        player.username = form.username.data
        player.gender = form.gender.data
        player.color = form.color.data
        db.session.commit()
        return render_template('players/get_player.html', player=player)
    return render_template("players/get_player.html", player=player, form=form)