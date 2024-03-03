from app import db
import sqlalchemy as sa
from random import choice

from app.models import TarotGame

emojis = '🐶🐱🐭🐹🐰🦊🐻🐼🐻‍❄️🐨🐯🦁🐮🐷🐸🐵🙈🙉🙊🐒🐔🐧🐦🐤🐣🐥🦆🐦‍🦅🦉🦇🐺🐗🐴🦄🐝🪱🐛🦋🐌🐞🦂🐢🐍🦎🦖🦕🐙🦑🦐🦞🦀🐡🐠🐟🐬🐳🐋🦈🦭🐊🐅🐆🦓🦍🦧🦣🐘🦛🦏🐪🐫🦒🦘🦬🐃🐂🐄🐎🐖🐏🐑🦙🐐🦌🐕🐩🦮🐕‍🦺🐈🐈‍⬛🐓🦃🦤🦚🦜🦢🦩🕊️🐇🦝🦨🦡🦫🦦🦥🐁🐀🐿️🦔🐉🐲'

def get_random_unique_emoji():
    emoji = choice(emojis)
    tarot_game = db.session.scalar(sa.select(TarotGame).where(TarotGame.game_name == emoji))
    while tarot_game:
        emoji = choice(emojis)
        tarot_game = db.session.scalar(sa.select(TarotGame).where(TarotGame.game_name == emoji))
    return emoji