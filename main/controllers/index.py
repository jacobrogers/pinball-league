from main.controllers import *

class IndexView(BaseView):
    
    def doGet(self, request):
        if (request.user.is_authenticated()) and not request.user.is_superuser:
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
                return {'player': player, 'group': group, 'rank': ranking[0].rank}
            else:
                return rankings_page
        except Player.DoesNotExist:
            None
        except League_Game.DoesNotExist:
            None

    def rankings_page(self):
        players = Player.objects.all()
        for player in players:
            total_points = 0
            for game in League_Game.objects.filter(player=player):
                points = game.league_points if game.league_points is not None else 0
                bonus_points = game.bonus_points if game.bonus_points is not None else 0
                total_points = total_points + (points + bonus_points)   
            player.total_points = total_points
        weeks = [game.group.week for game in League_Game.objects.all()]
        week = max(weeks) if weeks else 1
        return {'week': week, 'players': players}