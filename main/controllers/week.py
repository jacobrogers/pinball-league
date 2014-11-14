from main.controllers import *

class WeekView(BaseView):
    template = 'week.html'

    def get(self, request, week):
        groups = Group.objects.filter(week=week)

        if not groups:
            message = 'Week %s has not started yet.' % week
            return self.error_page(request, message)

        model_groups = []
        for g in groups:
            group = {'tables': [], 'players': [], 'group': g.group}
            group['canEnterScores'] = self.user_can_enter_scores(request.user, week, group['group']) if request.user.is_authenticated() else False

            for game in g.games.all():
                if game.table not in group['tables']:
                    group['tables'].append(game.table)
                if game.player not in group['players']:
                    group['players'].append(game.player)
                    game.player.points = 0
            if not g.is_open:
                for game in g.games.all():
                    game.player.points = game.total_points if game.total_points != None else None
                    for player in group['players']:
                        if player == game.player and game.total_points != None:
                            player.points = player.points + game.total_points
                            break
            model_groups.append(group)

        model = {'week': week, 'groups': model_groups}
        self.addWeeksToModel(model)
        return render(request, self.template, model)