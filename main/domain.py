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

def group_players(players):
    def grouper(iterable, n, fillvalue=None):
        "Collect data into fixed-length chunks or blocks"
        from itertools import izip_longest
        # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
        args = [iter(iterable)] * n
        return izip_longest(fillvalue=fillvalue, *args)
    
    return [{'players': group, 'tables': []} for group in grouper(players, 4)]

