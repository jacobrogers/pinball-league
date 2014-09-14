from main.controllers import * 

class BaseView(View):
    template = 'index.html'

    def get(self, request, *args, **kwargs):
        model = self.doGet(request)
        self.addWeeksToModel(model)
        self.addTutorials(model)
        return render(request, self.template, model)

    def doGet(self, request):
        print 'doGet not overrided'

    def error_page(self, request, message):
         return render(request, 'error.html', {'message': message})

    def addWeeksToModel(self, model):
        weeks = [group.week for group in Group.objects.distinct('week')]
        model['weeks'] = weeks
        return model

    def addTutorials(self, model):
        tutorials = Table.objects.exclude(tutorial='')
        model['tutorials'] = tutorials

    def user_can_enter_scores(self, user, week, group):
        weeks = [g.week for g in Group.objects.distinct('week')]
        isCurrentWeek = max(weeks) == int(week)
        if user.is_superuser and isCurrentWeek:
            return True
        
        player = Player.objects.filter(user=user)
        modelGroup = Group.objects.filter(group=group, week=week)
        games = League_Game.objects.filter(player=player, group=modelGroup)
        return games and isCurrentWeek
