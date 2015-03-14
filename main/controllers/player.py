from main.controllers import *

class PlayerView(BaseView):
    template = 'player.html'

    def get(self, request, id):
        try:
            player = Player.objects.get(id=id)
        except Player.DoesNotExist:
            message = 'Player not found.  Find players <a href="/players">here</a>.'
            return self.error_page(request, message)
            
        games = player.games.all()
        player_games = []
        for table in sorted({game.table for game in games}, key=attrgetter('name')):
            game = {'table': {'name': table.name, 'id': table.id} }
            game['scores'] = sorted([{'week': g.group.week, 'score': g.score} for g in games if g.table == table], key=itemgetter('score'), reverse=True)
            player_games.append(game)

        week_points = {}
        for game in games:
            if game.group.week in week_points:
                week_points[game.group.week]['league_points'] = game.league_points + week_points[game.group.week]['league_points']
            else:
                week_points[game.group.week] = {'group': game.group, 'league_points': game.league_points}
        
        model = {'player': player, 'games': player_games, 'week_points': week_points}
        self.addWeeksToModel(model)
        model['opponents'] = self.create_head_to_head(player)
        return render(request, self.template, model)

    def create_head_to_head(self, player):
        opponents = {}
        for group in player.groups.all():
            for opponent in group.players.all():
                if opponent != player:
                    for opponent_game in League_Game.objects.filter(group=group, player=opponent):
                        if opponent not in opponents:
                            opponents[opponent] = {'wins': 0, 'losses': 0}
                            
                        player_game = League_Game.objects.get(group=group, player=player, table=opponent_game.table)
                    
                        field = 'wins' if player_game.score > opponent_game.score else 'losses'
                        opponents[opponent][field] = opponents[opponent][field] + 1
        return opponents

class PlayersView(BaseView):
    template = 'players.html'

    def doGet(self, request):
        players = Player.objects.all()
        return {'players': players}
