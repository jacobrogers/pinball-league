from main.controllers import *

class RankingsView(BaseView):
	template = 'rankings.html'

	def doGet(self, request):
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