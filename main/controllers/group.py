from main.controllers import *

class GroupView(BaseView):
    template = 'group.html'

    def doGet(self, request):
        (week, group) = (request.GET.get('week'), request.GET.get('group'))
        canEnterScores = self.user_can_enter_scores(request.user, week, group) if request.user.is_authenticated() else False
        return {'week': week, 'group': group, 'canEnterScores': canEnterScores}

class SaveGamesApiView(BaseView):

    def post(self, request):
        payload = json.loads(request.body)
        players = payload['players']
        group = payload['group']
        week = payload['week']
        tableModel = Table.objects.get(id=payload['table']['id'])
        groupModel = Group.objects.get(group=group)

        scores = sorted([int(player['score']) for player in players],reverse=True)
        points = []
        for player in players:
            playerModel = Player.objects.get(id=player['id'])
            # savedGame = League_Game.objects.get(group=group, week=week, player=player)
            game = League_Game(player=playerModel, group=groupModel, table=tableModel, score=player['score'])
            game.league_points = decide_points(scores, game.score)
            game.save()
            points.append({'id': player['id'], 'league_points': game.league_points})
        return json_response(points, 201)
