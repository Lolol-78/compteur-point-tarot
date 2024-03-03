from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from datetime import datetime, timezone
from app import db, app


players_many_to_many = sa.Table("players",
                                db.metadata,
                                sa.Column("tarotGame_id", sa.Integer, sa.ForeignKey("tarot_game.id"), primary_key=True),
                                sa.Column("player_id", sa.Integer, sa.ForeignKey("player.id"), primary_key=True))


class TarotGame(db.Model):
    __tablename__ = "tarot_game"
    
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    
    game_name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    
    players: so.WriteOnlyMapped['Player'] = so.relationship(
        secondary=players_many_to_many,
        back_populates='games')
    
    deals: so.WriteOnlyMapped['Deal'] = so.relationship(back_populates="game")
    
    creation_date: so.Mapped[Optional[datetime]] = so.mapped_column(sa.DateTime(), default=lambda: datetime.now(timezone.utc))
    last_accessed: so.Mapped[Optional[datetime]] = so.mapped_column(sa.DateTime(), default=lambda: datetime.now(timezone.utc))
    
    def add_player(self, player):
        self.players.add(player)
    
    def remove_player(self, player):
        self.players.remove(player)
    
    def __repr__(self):
        return '<Game {}>'.format(self.game_name)

class Player(db.Model):
    __tablename__ = "player"
    
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    
    username: so.Mapped[str] = so.mapped_column(sa.String(64), unique=True, index=True)
    
    #0: ♂, 1: ♀
    gender: so.Mapped[int] = so.mapped_column(sa.Integer)
    
    color: so.Mapped[str] = so.mapped_column(sa.String(20))
    
    games: so.WriteOnlyMapped['TarotGame'] = so.relationship(
        secondary=players_many_to_many,
        back_populates="players")
    
    annonces: so.WriteOnlyMapped['Annonce'] = so.relationship(back_populates="player")
    
    def __repr__(self) -> str:
        return '<Player {}>'.format(self.username)

class Deal(db.Model):
    __tablename__ = "deal"
    
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    
    game_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey(TarotGame.id, name="fk_game_tarot_game"), index=True)
    game: so.Mapped[TarotGame] = so.relationship(back_populates="deals")
    
    dealer_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey(Player.id, name="fk_dealer_player"), index=True)
    dealer: so.Mapped[Player] = so.relationship(foreign_keys=[dealer_id])
    
    called_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey(Player.id, name="fk_called_player"), index=True)
    called: so.Mapped[Player] = so.relationship(foreign_keys=[called_id])
    
    annonces: so.WriteOnlyMapped['Annonce'] = so.relationship(back_populates="deal")
    
    nb_oudlers: so.Mapped[int] = so.mapped_column(sa.Integer, default=0)
    
    nb_points: so.Mapped[int] = so.mapped_column(sa.Integer, default=0)
    
    announcement: so.Mapped[int] = so.mapped_column(sa.Integer, default=0)
    
    created: so.Mapped[datetime] = so.mapped_column(sa.DateTime, default=lambda: datetime.now(timezone.utc))

class Annonce(db.Model):
    
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    
    deal_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey(Deal.id, name="fk_deal_annonce"), index=True)
    deal: so.Mapped[Deal] = so.relationship(back_populates="annonces")
    
    valeur: so.Mapped[int] = so.mapped_column(sa.Integer, default=0)
    
    player_id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, sa.ForeignKey(Player.id, name="fk_player_annonce"), index=True)
    player: so.Mapped[Player] = so.relationship(back_populates="annonces")