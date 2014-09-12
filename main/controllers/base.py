from main.controllers import * 

class BaseView(View):
    template = 'index.html'

    def get(self, request, *args, **kwargs):
        model = self.doGet(request)
        self.addWeeksToModel(model)
        return render(request, self.template, model)

    def doGet(self, request):
        print 'doGet not overrided'

    def addWeeksToModel(self, model):
        weeks = [group.week for group in Group.objects.distinct('week')]
        model['weeks'] = weeks
        return model

    def user_can_enter_scores(self, user, week, group):
        weeks = [g.week for g in Group.objects.distinct('week')]
        isCurrentWeek = max(weeks) == int(week)
        if user.is_superuser and isCurrentWeek:
            return True
        
        player = Player.objects.filter(user=user)
        modelGroup = Group.objects.filter(group=group, week=week)
        games = League_Game.objects.filter(player=player, group=modelGroup)
        return games and isCurrentWeek
