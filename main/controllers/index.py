from main.controllers import *

class IndexView(BaseView):
    template = 'index.html'

    def doGet(self, request):
        weeks = [group.week for group in Group.objects.distinct('week')]
        currentWeek = max(weeks) if weeks else 1

        if (request.user.is_authenticated()):
            try:
                player = Player.objects.get(user=request.user)
                group_model = League_Game.objects.filter(player=player, group__week=currentWeek).distinct('group__group')[0].group
                group = {'group': group_model.group, 'week': currentWeek, 'tables': [], 'players': []}
                for game in group_model.games.all():
                    if game.table not in group['tables']:
                        group['tables'].append(game.table)
                    if game.player not in group['players']:
                        group['players'].append(game.player)
                self.template = 'user_home.html'
                return {'player': player, 'group': group}
            except Player.DoesNotExist:
                None
            except League_Game.DoesNotExist:
                None
        
        rankings = [ranking.week for ranking in Ranking.objects.all()]
        week = max(rankings) if rankings else 1
        rankings = Ranking.objects.filter(week=week)
        return {'week': week, 'weeks': weeks, 'rankings': rankings} 
        