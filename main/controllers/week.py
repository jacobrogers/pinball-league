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
            group = {'tables': [], 'group': g.group}
            group['canEnterScores'] = self.user_can_enter_scores(request.user, week, group['group']) if request.user.is_authenticated() else False
            group['players'] = g.players.all()
            for game in g.games.all():
                if game.table not in group['tables']:
                    group['tables'].append(game.table)
            if not g.is_open:
                for game in g.games.all():
                    for player in group['players']:
                        if player == game.player and game.league_points != None:
                            player.week_points = player.week_points + game.league_points
                            break
            for player in group['players']:
                rank = player.rankings.get(week=week)
                player.rank = rank.rank
            model_groups.append(group)

        model = {'week': week, 'groups': model_groups}
        print model
        self.addWeeksToModel(model)
        return render(request, self.template, model)