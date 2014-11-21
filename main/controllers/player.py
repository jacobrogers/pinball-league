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
                week_points[game.group.week]['total_points'] = game.total_points + week_points[game.group.week]['total_points']
            else:
                week_points[game.group.week] = {'group': game.group, 'total_points': game.total_points}
        print week_points
        model = {'player': player, 'games': player_games, 'week_points': week_points}
        self.addWeeksToModel(model)
        return render(request, self.template, model)

class PlayersView(BaseView):
    template = 'players.html'

    def doGet(self, request):
        players = Player.objects.all()
        return {'players': players}
