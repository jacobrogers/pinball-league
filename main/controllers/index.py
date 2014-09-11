from main.controllers import BaseView, Group, Ranking

class IndexView(BaseView):
    template = 'index.html'

    def doGet(self, request):
        weeks = [group.week for group in Group.objects.distinct('week')]
        maxWeek = max(weeks) if weeks else 1

        rankings = [ranking.week for ranking in Ranking.objects.all()]
        week = max(rankings) if rankings else 1
        rankings = Ranking.objects.filter(week=week)
        return {'week': week, 'weeks': weeks, 'rankings': rankings}
