from app import app, db
from flask import render_template, flash, redirect, url_for, request
import sqlalchemy as sa
from datetime import datetime, timezone
from app.models import TarotGame, Player, Deal, Annonce
from app.forms import NewTarotGameForm, NewPlayerForm, EditPlayerForm, EditDealForm, EditTarotGamePlayer, EditDealAnnonceForm
from app.emoji import get_random_unique_emoji
from app.tarot_func import get_line_chart_datasets, get_called_pie_chart_dataset, get_dealers_pie_chart_dataset, get_win_bar_chart_dataset, get_annonce_bar_chart_dataset

ANNONCES = ['fait une poignée', 'fait une double-poignée', 'fait une triple-poignée', 'a mis le petit au bout', "s'est fait prendre le petit au bout"]
ANNONCES_CHOICES = [(0, 'fait une poignée'), (1, 'fait une double-poignée'), (2, 'fait une triple-poignée'), (3, 'a mis le petit au bout'), (4, "s'est fait prendre le petit au bout")]
ANNOUNCEMENT = ["...", "petite", "garde", "garde-sans", "garde-contre"]

@app.route('/index')
def index():
    return redirect(url_for('games'))

@app.route('/')
def home():
    return redirect(url_for('games'))

@app.route('/games', methods=['POST', 'GET'])
def games():
    tarot_games = db.session.scalars(sa.select(TarotGame).order_by(TarotGame.creation_date.desc())).all()
    players_username = [[player.username for player in db.session.scalars(game.players.select()).all()] for game in tarot_games]
    
    return render_template('games.html', tarot_games=tarot_games, players_username=players_username, title="Parties")


@app.route('/new_tarot_game', methods=["POST", "GET"])
def new_tarot_game():
    players = db.session.scalars(sa.select(Player)).all()
    usernames = [player.username for player in players]
    form = NewTarotGameForm()
    form.player_1.choices=usernames
    form.player_2.choices=usernames
    form.player_3.choices=usernames
    form.player_4.choices=usernames
    form.player_5.choices=usernames
    if form.validate_on_submit():
        name = get_random_unique_emoji()
        tarot_game = TarotGame(game_name=name)
        tarot_game.players.add(db.session.scalar(sa.select(Player).where(Player.username == form.player_1.data)))
        tarot_game.players.add(db.session.scalar(sa.select(Player).where(Player.username == form.player_2.data)))
        tarot_game.players.add(db.session.scalar(sa.select(Player).where(Player.username == form.player_3.data)))
        tarot_game.players.add(db.session.scalar(sa.select(Player).where(Player.username == form.player_4.data)))
        tarot_game.players.add(db.session.scalar(sa.select(Player).where(Player.username == form.player_5.data)))
        d=Deal()
        tarot_game.deals.append(d)
        db.session.add(tarot_game)
        db.session.add(d)
        db.session.commit()
        flash(f"La partie {name} a été créé!")
        return redirect(url_for("game", game_id=tarot_game.id))
    return render_template("new_tarot_game.html", form=form, title="Nouvelle Partie")


@app.route("/new_player", methods=["POST", "GET"])
def new_player():
    form = NewPlayerForm()
    if form.validate_on_submit():
        player = Player(username=form.username.data, gender=form.gender.data, color=request.form.get("color"))
        db.session.add(player)
        db.session.commit()
        flash(f"Le joueur {player.username} a bien été créé !")
        return redirect(url_for("index"))
    return render_template("new_player.html", form=form, title="Nouveau Joueur")


@app.route('/players')
def players():
    p = db.session.scalars(sa.select(Player)).all()
    return render_template("players.html", players=p, title="Joueurs")

@app.route('/players/<player_id>/get_edit')
def get_edit_player(player_id):
    player = db.session.get(Player, int(player_id))
    form = EditPlayerForm(username=player.username, gender=player.gender, color=player.color)
    return render_template("get_player.html", player=player, form=form)

@app.route('/players/<int:player_id>/get_normal')
def get_normal_player(player_id):
    player = db.session.get(Player, player_id)
    if player is None:
        return None
    return render_template("get_player.html", player=player)

@app.route('/players/<int:player_id>/edit', methods=["POST", "GET"])
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
        return render_template('get_player.html', player=player)
    return render_template("get_player.html", player=player, form=form)

@app.route('/game/<int:game_id>', methods=["POST", "GET"])
def game(game_id):
    g = db.session.get(TarotGame, game_id)
    if g is None:
        return redirect(url_for("index"))
    g.last_accessed = datetime.now(timezone.utc)
    db.session.commit()
    deals = g.deals
    players = db.session.scalars(g.players.select()).all()
    annonces = []
    for deal in deals:
        annonce = deal.annonces
        annonces.append(annonce)
    line_chart_datasets = get_line_chart_datasets(players, deals, annonces)
    called_pie_chart_dataset = get_called_pie_chart_dataset(deals, players)
    dealer_pie_chart_dataset = get_dealers_pie_chart_dataset(deals, players)
    win_bar_chart_dataset = get_win_bar_chart_dataset(deals, players, annonces)
    annonce_bar_chart_dataset = get_annonce_bar_chart_dataset(deals, players, annonces)
    return render_template("game.html", game=g, 
                                        players=players, 
                                        deals=deals, 
                                        announcement=ANNOUNCEMENT, 
                                        annonces=annonces, 
                                        annonces_label=ANNONCES, 
                                        line_chart_datasets=line_chart_datasets, 
                                        called_pie_chart_dataset=called_pie_chart_dataset, 
                                        dealer_pie_chart_dataset=dealer_pie_chart_dataset,
                                        win_bar_chart_dataset=win_bar_chart_dataset,
                                        annonce_bar_chart_dataset=annonce_bar_chart_dataset)

@app.route('/game/<game_id>/get_edit_players')
def game_get_edit_player(game_id):
    game = db.session.get(TarotGame, int(game_id))
    if game is None:
        return None
    players = db.session.scalars(game.players.select()).all()
    all_usernames = [player.username for player in db.session.scalars(sa.select(Player)).all()]
    form = EditTarotGamePlayer()
    form.player_1.choices=all_usernames
    form.player_2.choices=all_usernames
    form.player_3.choices=all_usernames
    form.player_4.choices=all_usernames
    form.player_5.choices=all_usernames
    form.player_1.data=players[0].username 
    form.player_2.data=players[1].username
    form.player_3.data=players[2].username 
    form.player_4.data=players[3].username
    form.player_5.data=players[4].username
    return render_template("game_edit_player.html", game=game, players=players, form=form)

@app.route('/game/<int:game_id>/edit_players', methods=["GET", "POST"])
def game_edit_players(game_id):
    game = db.session.get(TarotGame, game_id)
    if game is None:
        return None
    players = db.session.scalars(game.players.select()).all()
    all_usernames = [player.username for player in db.session.scalars(sa.select(Player)).all()]
    form = EditTarotGamePlayer()
    form.player_1.choices=all_usernames
    form.player_2.choices=all_usernames
    form.player_3.choices=all_usernames
    form.player_4.choices=all_usernames
    form.player_5.choices=all_usernames
    if form.validate_on_submit():
        deals = game.deals
        olds = []
        news = []
        for i in range(5):
            player = db.session.scalar(sa.select(Player).where(Player.username == getattr(getattr(form, f"player_{i+1}"), "data")))
            if player != players[i]:
                olds.append(players[i])
                news.append(player)
        if olds != []:
            for deal in deals:
                if deal.dealer in olds:
                    deal.dealer = None #news[olds.index(deal.dealer)]
                if deal.called in olds:
                    deal.called = None #news[olds.index(deal.called)]
            for player in olds:
                game.players.remove(player)
            for player in news:
                game.players.add(player)
            db.session.commit()
            deals = game.deals
        players = db.session.scalars(game.players.select()).all()
        return render_template("game_edit_player.html", game=game, players=players)
    return render_template("game_edit_player.html", game=game, players=players, form=form)

@app.route('/game/<int:game_id>/get_players')
def game_get_players(game_id):
    game = db.session.get(TarotGame, game_id)
    if game is None:
        return
    else:
        players = db.session.scalars(game.players.select()).all()
        return render_template("game_edit_player.html", game=game, players=players)

@app.route('/game/<int:game_id>/<int:deal_id>/get_edit_deal')
def game_get_edit_deal(game_id, deal_id):
    game = db.session.get(TarotGame, game_id)
    deal = db.session.get(Deal, deal_id)
    if game is None or not deal in game.deals:
        return None
    player_usernames = [""] + [player.username for player in db.session.scalars(game.players.select()).all()]
    announcement = [(0, ""), (1, "petite"), (2, "garde"), (3, "garde-sans"), (4, "garde-contre")]
    form = EditDealForm()
    form.dealer.choices = player_usernames
    form.dealer.data = deal.dealer.username if deal.dealer else ""
    form.called.choices = player_usernames
    form.called.data = deal.called.username if deal.called else ""
    form.announcement.choices = announcement
    form.announcement.data = str(deal.announcement)
    form.nb_oudlers.data = deal.nb_oudlers
    form.nb_points.data = deal.nb_points
    for annonce in deal.annonces:
        form.annonces.append_entry()
        form.annonces.entries[-1].player.choices = player_usernames
        form.annonces.entries[-1].player.data = annonce.player.username if annonce.player else ""
        form.annonces.entries[-1].annonce.data = str(annonce.valeur)
    return render_template("game_edit_deal.html", game=game, deal=deal, form=form)

@app.route('/game/<int:game_id>/<int:deal_id>/edit_deal', methods=["POST", "GET"])
def game_edit_deal(game_id, deal_id):
    game = db.session.get(TarotGame, game_id)
    deal = db.session.get(Deal, deal_id)
    if not deal in game.deals or game is None:
        return
    player_usernames = [""] + [player.username for player in db.session.scalars(game.players.select()).all()]
    announcement = [(0, ""), (1, "petite"), (2, "garde"), (3, "garde-sans"), (4, "garde-contre")]
    form = EditDealForm()
    form.dealer.choices = player_usernames
    form.called.choices = player_usernames
    form.announcement.choices = announcement
    form.game = game
    if form.validate_on_submit():
        
        valid = True
        for annonce in form.annonces.entries:
            if annonce.player.data == "":
                annonce.player.errors = ("Un joueur est necessaire", )
                valid = False
            player = db.session.scalar(game.players.select().where(Player.username == annonce.player.data))
            if player is None:
                annonce.player.errors = ("Joueur non valide", )
                valid = False
            if not 0 <= int(annonce.annonce.data) <= len(ANNONCES):
                annonce.annonce.errors = ('Mauvaise annonce', )
                valid = False
        
        if valid:
            deal.dealer = db.session.scalar(game.players.select().where(Player.username == form.dealer.data))
            deal.called = db.session.scalar(game.players.select().where(Player.username == form.called.data))
            deal.announcement = form.announcement.data
            deal.nb_oudlers = form.nb_oudlers.data
            deal.nb_points = form.nb_points.data
            annonces = deal.annonces
            for i in range(len(annonces)):
                annonces[i].player = db.session.scalar(game.players.select().where(Player.username == form.annonces.entries[i].player.data))
                annonces[i].valeur = int(form.annonces.entries[i].annonce.data)
            db.session.commit()
            players = db.session.scalars(game.players.select()).all()
            annonces = deal.annonces
            return render_template("game_edit_deal.html", game=game, deal=deal, annonces=annonces, annonces_label=ANNONCES, announcement=ANNOUNCEMENT, players=players)
        
    for annonce in form.annonces.entries:
            if annonce.player.data == "":
                annonce.player.errors = ("Un joueur est necessaire", )
            player = db.session.scalar(game.players.select().where(Player.username == annonce.player.data))
            if player is None:
                annonce.player.errors = ("Joueur non valide", )
            if not 0 <= int(annonce.annonce.data) <= len(ANNONCES):
                annonce.annonce.errors = ('Mauvaise annonce', )
    return render_template("game_edit_deal.html", game=game, deal=deal, announcement=ANNOUNCEMENT, form=form)

@app.route('/game/<int:game_id>/<int:deal_id>/get_deal')
def game_get_deal(game_id, deal_id):
    game = db.session.get(TarotGame, game_id)
    deal = db.session.get(Deal, deal_id)
    if not deal in game.deals or game is None:
        return None
    announcement = ANNOUNCEMENT
    players = db.session.scalars(game.players.select()).all()
    annonces = deal.annonces
    annonces_label = ANNONCES
    return render_template("game_edit_deal.html", game=game, deal=deal, announcement=announcement, annonces=annonces, annonces_label=annonces_label, players=players)

@app.route('/game/<int:game_id>/<int:deal_id>/add_annonce', methods=['POST', 'GET'])
def game_deal_add_annonce(game_id: int, deal_id: int):
    game = db.session.get(TarotGame, game_id)
    if game is None:
        return None
    deal = db.session.get(Deal, deal_id)
    if not deal in game.deals:
        return None
    annonce = Annonce()
    deal.annonces.append(annonce)
    db.session.add(annonce)
    db.session.commit()
    
    player_usernames = [""] + [player.username for player in db.session.scalars(game.players.select()).all()]
    announcement = [(0, ""), (1, "petite"), (2, "garde"), (3, "garde-sans"), (4, "garde-contre")]
    form = EditDealForm()
    form.dealer.choices = player_usernames
    form.called.choices = player_usernames
    form.announcement.choices = announcement
    form.game = game
    form.validate = lambda *args, **kwargs: 1
    form.validate_on_submit()
    for annonce in form.annonces.entries:
        annonce.player.choices = player_usernames
    form.annonces.append_entry()
    form.annonces.entries[-1].player.choices = player_usernames
    form.annonces.entries[-1].player.data = ""
    form.annonces.entries[-1].annonce.data = 0
    return render_template("game_edit_deal.html", game=game, deal=deal, form=form)

@app.route('/game/<int:game_id>/<int:deal_id>/remove_annonce', methods=['POST', 'GET'])
def game_deal_remove_annonce(game_id: int, deal_id: int):
    game = db.session.get(TarotGame, game_id)
    if game is None:
        return
    deal = db.session.get(Deal, deal_id)
    if deal is None or not deal in game.deals:
        return
    annonces = deal.annonces
    last_annonce = annonces[-1]
    db.session.delete(last_annonce)
    db.session.commit()
    
    player_usernames = [""] + [player.username for player in db.session.scalars(game.players.select()).all()]
    announcement = [(0, ""), (1, "petite"), (2, "garde"), (3, "garde-sans"), (4, "garde-contre")]
    form = EditDealForm()
    form.dealer.choices = player_usernames
    form.called.choices = player_usernames
    form.announcement.choices = announcement
    form.game = game
    form.validate = lambda *args, **kwargs: 1
    form.validate_on_submit()
    for annonce in form.annonces.entries:
        annonce.player.choices = player_usernames
    form.annonces.pop_entry()
    return render_template("game_edit_deal.html", game=game, deal=deal, form=form)

@app.route('/game/<int:game_id>/new_deal')
def game_new_deal(game_id):
    game = db.session.get(TarotGame, game_id)
    if game is None:
        return None
    deal = Deal()
    game.deals.append(deal)
    db.session.commit()
    return render_template("game_new_deal.html", game=game, deal=deal, announcement=ANNOUNCEMENT)

@app.route('/game/<int:game_id>/get_graphics')
def game_get_graphics(game_id):
    game = db.session.get(TarotGame, game_id)
    players = db.session.scalars(game.players.select()).all()
    deals = game.deals
    annonces = [deal.annonces for deal in deals]
    line_chart_datasets = get_line_chart_datasets(players, deals, annonces)
    called_pie_chart_dataset = get_called_pie_chart_dataset(deals, players)
    dealer_pie_chart_dataset = get_dealers_pie_chart_dataset(deals, players)
    win_bar_chart_dataset = get_win_bar_chart_dataset(deals, players, annonces)
    annonce_bar_chart_dataset = get_annonce_bar_chart_dataset(deals, players, annonces)
    return render_template("game_get_graphics.html", line_chart_datasets=line_chart_datasets, called_pie_chart_dataset=called_pie_chart_dataset, dealer_pie_chart_dataset=dealer_pie_chart_dataset, win_bar_chart_dataset=win_bar_chart_dataset, annonce_bar_chart_dataset=annonce_bar_chart_dataset)

@app.route('/game/<int:game_id>/delete')
def game_delete(game_id: int):
    game = db.session.get(TarotGame, game_id)
    if game is None:
        flash("La partie n'existe pas")
        return redirect(url_for("game", game_id=game_id))

    db.session.delete(game)
    db.session.commit()
    return redirect(url_for("games"))