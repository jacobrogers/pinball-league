from main.controllers import *

class SetupWeekView(BaseView):
    template = 'setup_week.html'

    def doGet(self, request):
        groups = Group.objects.all().aggregate(Max('week'))
        week = groups['week__max']+1 if groups['week__max'] else 1
        open_groups = Group.objects.filter(games__score=None).distinct('group')
        return {'week': week, 'open_groups': open_groups}
        
class SetupWeekApiView(BaseView):
    
    def get(self, request, week):
        model = {}
        if int(week) == 1:
            model['players'] = [basic_json(player) for player in Player.objects.all()]
        else:
            players = League_Game.objects.filter(group__week=int(week)-1).values('group__group', 'player').annotate(points=Sum('league_points'))
            groups = {group+1: [] for group in range(len({player['group__group'] for player in players}))}
            for player in players:
                real_player = Player.objects.get(id=player['player'])
                total_points = sum([p.league_points for p in real_player.games.all()])
                groups[player['group__group']].append({'name': real_player.name, 'id': real_player.id, 'league_points': player['points'], 'total_points': total_points})
            model['groups'] = group_players(groups)
            model['players'] = [basic_json(player) for player in Player.objects.all() if not self.player_has_game(players, player)]
        return json_response(model)

    def post(self, request, week):
        payload = json.loads(request.body) 
        self.saveGroups(week, payload['groups'])
        return HttpResponse(status=201)        

    def saveGroups(self, week, groups):
        for i, g in enumerate(groups):            
            group = Group(week=week, group=i+1)
            group.save()
            for player in [Player.objects.get(id=player['id']) for player in g['players']]:
                group.players.add(player)
                rank = next( (p['rank'] for p in g['players'] if p['id'] == player.id), None )
                self.assignRank(player, week, rank)
    def player_has_game(self, players, player):
        for p in players:
            if p['player'] == player.id:
                return True
        return False
        
    def assignRank(self, player, week, rank):
        total_points = 0
        for game in League_Game.objects.filter(player=player):
            points = game.league_points if game.league_points is not None else 0
            total_points = total_points + points
        
        ranking = Ranking(player=player, week=week, points=total_points, rank=rank)
        ranking.save()
