from main.controllers import *
from decimal import *

class DivisionsView(BaseView):
	template = 'divisions.html'

	def doGet(self, request):
		players = []
		for player in Player.objects.filter(status='Active'):
			games = player.games.all()
			avg_group = -1
			if games:
				avg_group = Decimal(sum([game.group.group for game in games])) / Decimal(len(games))
			player.average_group = avg_group
			if player.average_group > 0:
				players.append(player)
		return {'players': players}
