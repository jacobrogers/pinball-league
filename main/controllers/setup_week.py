from main.controllers import BaseView, Player, Group, League_Game, Table, Ranking, render, Max, Sum, basic_json, group_players, json_response, json, HttpResponse

class SetupWeekView(BaseView):
    template = 'setup_week.html'

    def doGet(self, request):
        groups = Group.objects.all().aggregate(Max('week'))
        week = groups['week__max']+1 if groups['week__max'] else 1
        open_groups = Group.objects.filter(games__score=None).distinct('group')
        return {'week': week, 'open_groups': open_groups}
        
class SetupWeekApiView(BaseView):
    def get(self,request, week):
        players = League_Game.objects.filter(group__week=int(week)-1).values('group__group', 'player').annotate(points=Sum('league_points', field='league_points+bonus_points'))
        groups = {group+1: [] for group in range(len({player['group__group'] for player in players}))}
        for player in players:
            real_player = Player.objects.get(id=player['player'])
            groups[player['group__group']].append({'name': real_player.name, 'id': real_player.id, 'league_points': player['points']})
        new_players = [basic_json(player) for player in Player.objects.all() if not self.player_has_game(players, player)]
        model = {'groups': group_players(groups), 'players': new_players}
        return json_response(model)

    def post(self, request, week):
        payload = json.loads(request.POST.dict().keys()[0])
        print payload['groups']
        for i, g in enumerate(payload['groups']):            
            # print 'creating group', i+1, g
            group = Group()
            group.week = week
            group.group = i+1
            group.save()
            players = [Player.objects.get(id=player['id']) for player in g['players']]
            tables = [Table.objects.get(id=table['id']) for table in g['tables']]
            # print 'players',players
            # print 'tables',tables
            for (player, table) in [(player, table) for player in players for table in tables ]:
                game = League_Game()
                game.player = player
                game.table = table
                game.group = group
                game.save()
                # print 'creating game',game
            for player in players:
                ranking = Ranking()
                ranking.player = player
                ranking.week = week
                for p in g['players']:
                    if p['id'] == player.id:
                        ranking.rank = p['rank']
                        total_points = 0
                        for game in League_Game.objects.filter(player=player):
                            points = game.league_points if game.league_points is not None else 0
                            bonus_points = game.bonus_points if game.bonus_points is not None else 0
                            total_points = total_points + (points + bonus_points)
                        ranking.points = total_points
                # print 'creating rank',ranking
                ranking.save()
        return HttpResponse(status=201)

    def player_has_game(self,players, player):
        for p in players:
            if p['player'] == player.id:
                return True
        return False