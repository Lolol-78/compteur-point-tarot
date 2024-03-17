from app.models import Deal, Player, Annonce

CONSTRACT_POINTS = 25
VALUE_POIGNE = (20, 30, 40)
VALUE_PETIT_AU_BOUT = 10
REQUIRED_POINTS = (56, 51, 41, 36)


get_sign = lambda nb: 1 if nb>=0 else -1

def calculate_points_for_deal(players: 'list[Player]', deal: Deal, annonces: 'list[Annonce]'):
    player_dict = {}
    if deal.called == None or deal.dealer == None or deal.announcement == None:
        return False
    required_points = REQUIRED_POINTS[deal.nb_oudlers]
    bonus_points = abs(required_points - deal.nb_points)
    points = (CONSTRACT_POINTS + bonus_points) * [0, 1, 2, 4, 6][deal.announcement]
    sign = get_sign(deal.nb_points - required_points)
    nb_player_in_defense = 0
    for player in players:
        if deal.dealer != player and player != deal.called:
            player_dict[player.username] = points * sign * (-1)
            nb_player_in_defense += 1
    if nb_player_in_defense == 3:
        player_dict[deal.dealer.username] = points * 2 * sign
        player_dict[deal.called.username] = points * sign
    else:
        player_dict[deal.dealer.username] = points * 4 * sign
    for annonce in annonces:
        annonce_sign = sign
        for player in players:
            player_in_defense = (player.username != deal.dealer.username and player.username != deal.called.username)
            if annonce.valeur < 3: # Si c'est une poignée
                if player_in_defense:
                    player_dict[player.username] += annonce_sign * VALUE_POIGNE[annonce.valeur] * (-1)
                elif player.username == deal.dealer.username:
                    if nb_player_in_defense == 3:
                        player_dict[player.username] += VALUE_POIGNE[annonce.valeur] * annonce_sign * 2
                    else:
                        player_dict[player.username] += VALUE_POIGNE[annonce.valeur] * annonce_sign * 4
                elif player.username == deal.called.username:
                    player_dict[player.username] += VALUE_POIGNE[annonce.valeur] * annonce_sign
            elif 2 < annonce.valeur < 5: # si c'est un petit au bout
                if player_in_defense:
                    player_dict[player.username] += annonce_sign * VALUE_PETIT_AU_BOUT * (-1)
                elif player.username == deal.dealer.username:
                    if nb_player_in_defense == 3:
                        player_dict[player.username] += VALUE_PETIT_AU_BOUT * annonce_sign * 2
                    else:
                        player_dict[player.username] += VALUE_PETIT_AU_BOUT * annonce_sign * 4
                elif player.username == deal.called.username:
                    player_dict[player.username] += VALUE_PETIT_AU_BOUT * annonce_sign
    return player_dict

def get_all_points(players: 'list[Player]', deals: 'list[Deal]', annonces: 'list[list[Annonce]]'):
    player_dict = {}
    player_win_dict = {}
    for player in players:
        player_dict[player.username] = [0]
        player_win_dict[player.username] = []
    for i in range(len(deals)):
        player_dict_2 = calculate_points_for_deal(players, deals[i], annonces[i])
        if player_dict_2 != False:
            for key, item in player_dict_2.items():
                player_dict[key].append(player_dict[key][-1]+item)
                player_win_dict[key].append(get_sign(item))
        else:
            return player_dict, player_win_dict
    return player_dict, player_win_dict

def get_line_chart_datasets(players: 'list[Player]', deals: 'list[Deal]', annonces: 'list[list[Annonce]]'):
    player_dict, _ = get_all_points(players, deals, annonces)
    datasets = []
    for key, item in player_dict.items():
        color = get_player_by_name(players, key).color
        datasets.append({
			'data' : item,
			'label' : f"{key}: {item[-1]}",
			'borderColor' : color,
			'fill' : False,
            'pointBackgroundColor': color,
            'datalabels': {
                'color': color
            }
        })
    labels = [i+1 for i in range(len(datasets[0]['data']))]
    return datasets, labels

def get_dealers_pie_chart_dataset(deals: 'list[Deal]', players: 'list[Player]'):
    dealers = {}
    for deal in deals:
        if deal.dealer == None or deal.announcement == 0 or deal.called == None:
            break
        if deal.dealer.username in dealers:
            dealers[deal.dealer.username] += 1
        else:
            dealers[deal.dealer.username] = 1
    items = dealers.items()
    datasets = [{
        "label": 'Dealers',
        "data": [item[1] for item in items],
        "backgroundColor": [get_player_by_name(players, item[0]).color for item in items],
        "hoverOffset": 4
        }]
    labels = [item[0] for item in items]
    return datasets, labels

def get_called_pie_chart_dataset(deals: 'list[Deal]', players: 'list[Player]'):
    called = {}
    for deal in deals:
        if deal.dealer == None or deal.announcement == 0 or deal.called == None:
            break
        if deal.called.username in called:
            called[deal.called.username] += 1
        else:
            called[deal.called.username] = 1
    items = called.items()
    datasets = [{
        "label": 'Called',
        "data": [item[1] for item in items],
        "backgroundColor": [get_player_by_name(players, item[0]).color for item in items],
        "hoverOffset": 4
        }]
    labels = [item[0] for item in items]
    return datasets, labels

def get_win_bar_chart_dataset(deals: 'list[Deal]', players: 'list[Player]', annonces: 'list[list[Annonce]]'):
    _, player_win_dict = get_all_points(players, deals, annonces)
    datasets = [{
        "label": 'Victoire',
        "data": [item[1].count(1) for item in player_win_dict.items()],
        "backgroundColor": "#008000",
        "hoverOffset": 4
        }, 
        {
        "label": 'Défaite',
        "data": [item[1].count(-1) for item in player_win_dict.items()],
        "backgroundColor": "#FFA500",
        "hoverOffset": 4
        }]
    labels = [item[0] for item in player_win_dict.items()]
    return datasets, labels

def get_annonce_bar_chart_dataset(deals: 'list[Deal]', players: 'list[Player]', annonces: 'list[list[Annonce]]'):
    _, player_win_dict = get_all_points(players, deals, annonces)
    deals_count = {}
    for i in range(len(deals)):
        if deals[i].dealer == None or deals[i].announcement == 0 or deals[i].called == None:
            break
        if str(deals[i].announcement) + ("win" if player_win_dict[deals[i].dealer.username][i] == 1 else "lose") in deals_count:
            deals_count[str(deals[i].announcement) + ("win" if player_win_dict[deals[i].dealer.username][i] == 1 else "lose")] += 1
        else:
            deals_count[str(deals[i].announcement) + ("win" if player_win_dict[deals[i].dealer.username][i] == 1 else "lose")] = 1
    items = deals_count.items()
    data_win = {}
    data_lose = {}
    for item in items:
        if item[0].endswith("win"):
            data_win[item[0][:-3]] = item[1]
        else:
            data_lose[item[0][:-4]] = item[1]
    labels = ["Petite", "Garde", "Garde-sans", "Garde-contre"]
    datasets = [{
        "label": 'Réussies',
        "data": [{"x": labels[int(item[0])-1], "y": data_win[item[0]]} for item in data_win.items()],
        "stack": "Stack 0",
        "backgroundColor": "#ADD8E6",
    },
    {
        "label": 'Perdues',
        "data": [{"x": labels[int(item[0])-1], "y": data_lose[item[0]]} for item in data_lose.items()],
        "stack": "Stack 1",
        "backgroundColor": "#FFC0CB",
    }]
    return datasets, labels

def get_player_by_name(players: 'list[Player]', username: str) -> Player:
    """
    Function to retrieve a player from a list of players by their username.
    
    :param players: a list of Player objects
    :param username: a string representing the username to search for
    :return: a Player object if found, otherwise None
    """
    for player in players:
        if player.username == username:
            return player