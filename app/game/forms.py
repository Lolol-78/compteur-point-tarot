from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, Form, FieldList, FormField
from wtforms.validators import DataRequired, NumberRange, Length, ValidationError
from app import app, db
from app.models import Player, Deal
import sqlalchemy as sa

ANNONCES_CHOICES = [(0, 'fait une poignée'), (1, 'fait une double-poignée'), (2, 'fait une triple-poignée'), (3, 'a mis le petit au bout'), (4, "s'est fait prendre le petit au bout")]



class NewTarotGameForm(FlaskForm):
    player_1 = SelectField("Joueur 1", validators=[DataRequired()])
    player_2 = SelectField("Joueur 2", validators=[DataRequired()])
    player_3 = SelectField("Joueur 3", validators=[DataRequired()])
    player_4 = SelectField("Joueur 4", validators=[DataRequired()])
    player_5 = SelectField("Joueur 5", validators=[DataRequired()])
    submit = SubmitField('Créer')
    
    def validate_player_1(self, player_1):
        if player_1.data in {self.player_2.data, self.player_3.data, self.player_4.data, self.player_5.data}:
            raise ValidationError("Tous les joueurs doivent être différents")
    
    def validate_player_2(self, player_2):
        if player_2.data in {self.player_1.data, self.player_3.data, self.player_4.data, self.player_5.data}:
            raise ValidationError("Tous les joueurs doivent être différents")
        
    def validate_player_3(self, player_3):
        if player_3.data in {self.player_2.data, self.player_1.data, self.player_4.data, self.player_5.data}:
            raise ValidationError("Tous les joueurs doivent être différents")
        
    def validate_player_4(self, player_4):
        if player_4.data in {self.player_2.data, self.player_3.data, self.player_1.data, self.player_5.data}:
            raise ValidationError("Tous les joueurs doivent être différents")
        
    def validate_player_5(self, player_5):
        if player_5.data in {self.player_2.data, self.player_3.data, self.player_4.data, self.player_1.data}:
            raise ValidationError("Tous les joueurs doivent être différents")



class EditDealAnnonceForm(FlaskForm):
    player = SelectField(validate_choice=False)
    annonce = SelectField(choices=ANNONCES_CHOICES)
    
    validate2 = FlaskForm.validate
    game = None
    
    def validate(self, *args, **kwargs):
        if self.game:
            self.validate2()
        else:
            pass

class EditDealForm(FlaskForm):
    dealer = SelectField(validate_choice=False)
    announcement = SelectField(validate_choice=False)
    called = SelectField(validate_choice=False)
    nb_oudlers = IntegerField(validators=[NumberRange(min=0, max=3, message="Entre 0 et 3")])
    nb_points = IntegerField(validators=[NumberRange(min=0, max=91, message="Entre 0 et 91")])
    annonces = FieldList(FormField(EditDealAnnonceForm)) 
    submit = SubmitField()
    game = None
    
    def validate_dealer(self, dealer):
        if dealer.data == "":
            raise ValidationError("Un joueur est requis")
        player = db.session.scalar(sa.select(Player).where(Player.username == dealer.data))
        if player is None:
            raise ValidationError("Ce joueur n'existe pas")
        if not player in db.session.scalars(self.game.players.select()).all():
            raise ValidationError("Ce joueur n'est pas dans la partie")
    
    def validate_called(self, called):
        if called.data == "":
            raise ValidationError("Un joueur est requis")
        player = db.session.scalar(sa.select(Player).where(Player.username == called.data))
        if player is None:
            raise ValidationError("Ce joueur n'existe pas")
        if not player in db.session.scalars(self.game.players.select()).all():
            raise ValidationError("Ce joueur n'est pas dans la partie")
    
    def validate_announcement(self, announcement):
        if announcement.data == 0:
            raise ValidationError("Une annonce est requise")
        if not announcement.data in "1234":
            raise ValidationError("L'annonce est mauvaise")


class EditTarotGamePlayer(FlaskForm):
    player_1 = SelectField("Joueur 1", validators=[DataRequired("Ce champs est obligatoire")])
    player_2 = SelectField("Joueur 2", validators=[DataRequired("Ce champs est obligatoire")])
    player_3 = SelectField("Joueur 3", validators=[DataRequired("Ce champs est obligatoire")])
    player_4 = SelectField("Joueur 4", validators=[DataRequired("Ce champs est obligatoire")])
    player_5 = SelectField("Joueur 5", validators=[DataRequired("Ce champs est obligatoire")])
    submit = SubmitField("Soumettre")
    
    def validate_player_1(self, player_1):
        if player_1.data in {self.player_2.data, self.player_3.data, self.player_4.data, self.player_5.data}:
            raise ValidationError("Tous les joueurs doivent être différents")
    
    def validate_player_2(self, player_2):
        if player_2.data in {self.player_1.data, self.player_3.data, self.player_4.data, self.player_5.data}:
            raise ValidationError("Tous les joueurs doivent être différents")
        
    def validate_player_3(self, player_3):
        if player_3.data in {self.player_2.data, self.player_1.data, self.player_4.data, self.player_5.data}:
            raise ValidationError("Tous les joueurs doivent être différents")
        
    def validate_player_4(self, player_4):
        if player_4.data in {self.player_2.data, self.player_3.data, self.player_1.data, self.player_5.data}:
            raise ValidationError("Tous les joueurs doivent être différents")
        
    def validate_player_5(self, player_5):
        if player_5.data in {self.player_2.data, self.player_3.data, self.player_4.data, self.player_1.data}:
            raise ValidationError("Tous les joueurs doivent être différents")