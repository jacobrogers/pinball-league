from main.models import Table, Player, Group, League_Game, Ranking

Ranking.objects.all().delete()
League_Game.objects.all().delete()
Group.objects.all().delete()
Table.objects.all().delete()
Player.objects.all().delete()

tables = [['Twilight Zone',2684, 'twilight-zone'], \
		      ['World Poker Tour', 5134, 'world-poker-tour'], \
          ['Terminator 3: Rise of the Machines', 4787, 'terminator-3-rise-of-the-machines'], \
          ['X-Men Pro', 5822, 'x-men'], \
          ['Tales From The Crypt', 2493, 'tales-from-the-crypt'], \
          ['AC/DC Pro', 5767, 'ac-dc'], \
          ['South Park', 4444, 'south-park'], \
          ['Metallica Pro', 6028, 'metallica'], \
          ['The Avengers Pro', 5938, 'the-avengers']]

for table in tables:
  t = Table(name=table[0], ipdb_id=table[1], pinside_name=table[2])
  t.save()
	
players = [['Josh Noble', 'JBO'],['Adam McKinnie', 'ZED'], ['Daniel Carpenter', 'DC'], \
           ['Jacob Rogers', 'JMR', 22206], ['Steven Franke'], ['Stefanie McCollum'], \
           ['Robert Ryan'], ['Daniel Goett'], ['Nathan Goett'], ['Kyle Felling'], ['Jordan Lamb'], \
           ['Sam Nelson'], ['Jeremy Calton'], ['Wes Upchurch'], ['Lonnie McDonald']]

for player in players:
	ifpa_id = player[2] if len(player) == 3 else None
	signature = player[1] if len(player) > 1 else None 
	p = Player(name=player[0], ifpa_id=ifpa_id, signature=signature)
	p.save()
