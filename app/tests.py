from app.models import *

def init(db):
    
    p1 = Player(username="Loic", gender=0, color="#ff0000")
    p2 = Player(username="Cyril", gender=1, color="#0000ff")
    p3 = Player(username="Timothee", gender=1, color="#00ff00")
    p4 = Player(username="Alexandre", gender=1, color="#ff00ff")
    p5 = Player(username="Lionel", gender=0, color="#ffff00")

    db.session.add(p1)
    db.session.add(p2)
    db.session.add(p3)
    db.session.add(p4)
    db.session.add(p5)

    g1 = TarotGame(players=[p1, p2, p3, p4, p5], game_name="Test_1")
    g2 = TarotGame(players=[p1, p2, p3, p4, p5], game_name="Test_2")
    
    db.session.add(g1)
    db.session.add(g2)
    
    d1 = Deal(dealer=p1, called=p2)
    d2 = Deal(dealer=p3, called=p4)
    d3 = Deal(dealer=p1, called=p2)
    d4 = Deal(dealer=p3, called=p4)
    
    g1.deals.append(d1)
    g1.deals.append(d2)
    g2.deals.append(d3)
    g2.deals.append(d4)
    
    db.session.add(d1)
    db.session.add(d2)
    db.session.add(d3)
    db.session.add(d4)
    
    a1 = Annonce(deal=d1, player=p1, valeur=0)
    a2 = Annonce(deal=d1, player=p2, valeur=1)
    a3 = Annonce(deal=d1, player=p3, valeur=2)
    
    db.session.add(a1)
    db.session.add(a2)
    db.session.add(a3)
    
    db.session.commit()