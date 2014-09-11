from main.controllers import Table, render, BaseView

class TablesView(BaseView):
    template = 'tables.html'

    def doGet(self, request):
        tables = Table.objects.all()
        return {'tables': tables}

class TableView(BaseView):
    template = 'table.html'

    def get(self, request, id):
        from operator import itemgetter, attrgetter
        table = Table.objects.get(id=id)
        games = []
        for game in sorted(table.games.all(), key=attrgetter('score'), reverse=True):
            games.append({'week': game.group.week, 'player': {'id': game.player.id, 'name': game.player.name}, 'score': game.score})
        model = {'table': table, 'games': games}
        self.addWeeksToModel(model)
        return render(request, self.template, model)
