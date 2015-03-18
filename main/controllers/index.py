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
            if (group_model):
                group_model = group_model[0].group
                group = {'group': group_model.group, 'week': currentWeek, 'players': group_model.players}
                return {'player': player, 'group': group}
            else:
                return self.rankings_page()
        except Player.DoesNotExist:
            None
        except League_Game.DoesNotExist:
            None

    def rankings_page(self):
        return self.rank_by_ladder()

    def rank_by_points(self):
        players = Player.objects.all()
        weeks = [game.group.week for game in League_Game.objects.all()]
        week = max(weeks) if weeks else 1
        return {'week': week, 'players': players}

    def rank_by_ladder(self):
        rankings = [ranking.week for ranking in Ranking.objects.all()]
        week = max(rankings) if rankings else 1
        rankings = Ranking.objects.filter(week=week).order_by('rank')
        return {'week': week, 'rankings': rankings}