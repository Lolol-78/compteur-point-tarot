import sqlalchemy as sa
import sqlalchemy.orm as so
from app import app, db
from app.models import TarotGame, Player, Deal


@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'TarotGame': TarotGame, 'Player': Player, 'Deal': Deal}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)