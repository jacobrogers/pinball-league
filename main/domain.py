def decide_points(scores, score):
    if score == scores[0]:
        return 3
    if score == scores[-1]:
        return 0
    if score == scores[1]:
        return 2
    return 1

def decide_bonus_points(scores, score):
    if len(scores) == 2:
        if score == scores[0]:
            return 1 if score > scores[1]*3 else 0
        if score == scores[1]:
            return 0 if scores[0] > scores[1]*3 else 1
    else:
        if score == scores[0]:
            return 1 if score > scores[1]+scores[2] else 0
        if len(scores) == 3:
            if score == scores[2]:
                return 0 if scores[0] > scores[1]+scores[2] else 1
        if len(scores) == 4:
            if score == scores[1]:
                return 1 if score > scores[2]+scores[3] else 0
            if score == scores[2]:
                return 0 if scores[0] > scores[1]+scores[2] else 1
            if score == scores[3]:
                return 0 if scores[1] > scores[2]+scores[3] else 1
        return 0

def decide_movement(group):
        players = sorted(group, key=lambda (player): player['league_points'])
        players[0]['direction'] = 'down'
        players[-1]['direction'] = 'up'
        if len(players) == 4:
            players[1]['direction'] = 'down'
            players[2]['direction'] = 'up'
        elif len(players) == 3:
            players[1]['direction'] = 'stay'
        
def group_players(groups):
    group_cnt = max(groups.keys())
    new_groups = {group: [] for group in groups.keys()}
    for (group, players) in groups.iteritems():
        decide_movement(players)
        for player in players:
            if player['direction'] == 'up':
                groupIndex = group-1 if group > 1 else group
                new_groups[groupIndex].append(player)
            elif player['direction'] == 'down':
                groupIndex = group+1 if group < group_cnt else group
                new_groups[groupIndex].append(player)
    for group in new_groups.keys():
        new_groups[group] = sorted(new_groups[group], reverse=True,key=lambda (player): player['league_points'])
    return new_groups