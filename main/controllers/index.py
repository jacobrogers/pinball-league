from main.controllers import *

class IndexView(BaseView):
    
    def doGet(self, request):
        if (request.user.is_authenticated()):
            self.template = 'user_home.html'
            return self.user_home_page(request)
        else:
            self.template = 'index.html'
            return self.rankings_page()

    def user_home_page(self, request):
        weeks = [group.week for group in Group.objects.distinct('week')]

        try:
            currentWeek = max(weeks) if weeks else 1
            player = Player.objects.get(user=request.user)
            group_model = League_Game.objects.filter(player=player, group__week=currentWeek).distinct('group__group')
            ranking = player.rankings.filter(week=currentWeek)
            if (group_model):
                group_model = group_model[0].group
                group = {'group': group_model.group, 'week': currentWeek, 'tables': [], 'players': []}
                for game in group_model.games.all():
                    if game.table not in group['tables']:
                        group['tables'].append(game.table)
                    if game.player not in group['players']:
                        group['players'].append(game.player)
                print ranking[0]
                return {'player': player, 'group': group, 'rank': ranking[0].rank}
        except Player.DoesNotExist:
            None
        except League_Game.DoesNotExist:
            None

    def rankings_page(self):
        weeks = [group.week for group in Group.objects.distinct('week')]
        week = max(weeks) if weeks else 1
        rankings = Ranking.objects.filter(week=week).order_by('rank')
        return {'week': week, 'weeks': weeks, 'rankings': rankings}