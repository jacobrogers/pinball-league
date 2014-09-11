from main.controllers import BaseView

class GroupView(BaseView):
    template = 'group.html'

    def doGet(self, request):
        (week, group) = (request.GET.get('week'), request.GET.get('group'))
        canEnterScores = self.user_can_enter_scores(request.user, week, group) if request.user.is_authenticated() else False
        return {'week': week, 'group': group, 'canEnterScores': canEnterScores}