from main.controllers import *

class RankingsView(BaseView):
	template = 'rankings.html'

	def doGet(self, request):
		rankings = [ranking.week for ranking in Ranking.objects.all()]
		week = max(rankings) if rankings else 1
		rankings = Ranking.objects.filter(week=week).order_by('rank')
		return {'week': week, 'rankings': rankings}