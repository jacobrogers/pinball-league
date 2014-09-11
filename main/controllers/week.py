from main.controllers import BaseView, Group, render, Max

class SetupWeekView(BaseView):
    template = 'setup_week.html'

    def doGet(self, request):
        groups = Group.objects.all().aggregate(Max('week'))   
        week = groups['week__max']+1 if groups['week__max'] else 1
        return {'week': week}

class WeekView(BaseView):
    template = 'week.html'

    def get(self, request, week):
        groups = Group.objects.filter(week=week)
        model_groups = []
        for g in groups:
            group = {'tables': [], 'players': [], 'group': g.group}
            group['canEnterScores'] = self.user_can_enter_scores(request.user, week, group['group']) if request.user.is_authenticated() else False

            for game in g.games.all():
                if game.table not in group['tables']:
                    group['tables'].append(game.table)
                if game.player not in group['players']:
                    group['players'].append(game.player)
            model_groups.append(group)

        model = {'week': week, 'groups': model_groups}
        self.addWeeksToModel(model)
        return render(request, self.template, model)