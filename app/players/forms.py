from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, Form, FieldList, FormField
from wtforms.validators import DataRequired, NumberRange, Length, ValidationError
from app import app, db
from app.models import Player, Deal
import sqlalchemy as sa

ANNONCES_CHOICES = [(0, 'fait une poignée'), (1, 'fait une double-poignée'), (2, 'fait une triple-poignée'), (3, 'a mis le petit au bout'), (4, "s'est fait prendre le petit au bout")]



class NewPlayerForm(FlaskForm):
    username = StringField('Nom', validators=[Length(min=0, max=20)])
    gender = SelectField('genre', choices=[(-1, ""), (0, '♂'), (1, '♀')], default=-1, validators=[DataRequired()])
    color =StringField('Couleur', default="#563d7c")
    submit = SubmitField('Ajouter')
    
    def validate_username(self, username):
        if username.data == "":
            raise ValidationError("Ce champ est obligatoire")
        player = db.session.scalar(sa.select(Player).where(Player.username == username.data))
        if player is not None:
            raise ValidationError('Ce joueur existe déjà')
    
    def validate_gender(self, gender):
        if gender.data == "-1":
            raise ValidationError("Un genre est necessaire pour les accords grammaticaux")
        if not gender.data in {"0", "1"}:
            raise ValidationError("Mais qu'est-ce que t'essayes de faire ?")


class EditPlayerForm(FlaskForm):
    username = StringField(validators=[Length(min=0, max=20)])
    gender = SelectField('Genre:', choices=[(0, '♂'), (1, '♀')])
    color = StringField('Couleur:')
    submit = SubmitField('Soumettre')
    player = None
    
    def validate_username(self, username):
        player = db.session.scalar(sa.select(Player).where(Player.username == username.data))
        print(self.player)
        print(username.data)
        if username.data == "":
            raise ValidationError("Ce champs est obligatoire")
        if player is not None and player.username != self.player.username:
            print(2)
            raise ValidationError("Ce nom est déjà pris")
