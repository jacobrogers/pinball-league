from main.controllers import *

class RankingsView(BaseView):
	template = 'rankings.html'

	def doGet(self, request):
		players = Player.objects.all()
		weeks = [game.group.week for game in League_Game.objects.all()]
		week = max(weeks) if weeks else 1
		return {'week': week, 'players': players}