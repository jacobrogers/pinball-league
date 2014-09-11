from main.controllers import BaseView, render, Player, attrgetter, itemgetter

class PlayerView(BaseView):
    template = 'player.html'

    def get(self, request, id):
        player = Player.objects.get(id=id)
        games = player.games.all()
        player_games = []
        for table in sorted({game.table for game in games}, key=attrgetter('name')):
            game = {'table': {'name': table.name, 'id': table.id} }
            game['scores'] = sorted([{'week': g.group.week, 'score': g.score} for g in games if g.table == table], key=itemgetter('score'), reverse=True)
            player_games.append(game)
        model = {'player': player, 'games': player_games}
        self.addWeeksToModel(model)
        return render(request, self.template, model)

class PlayersView(BaseView):
    template = 'players.html'

    def doGet(self, request):
        players = Player.objects.all()
        return {'players': players}
