from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import Client
import json

from main.models import Player, Group, League_Game, Table

def basic_json(value):
    return {'id': value.id, 'name': value.name}

class FetchGroupTestCase(TestCase):

	fixtures = ['initial_data']

	def test_fetch_group_no_games(self):
		group = self.create_group(1, 2)
		tables = [basic_json(table) for table in Table.objects.filter(status='Active')]
		players = [basic_json(player) for player in group.players.all()]
		
		response = self.fetch_response('api_group', group)

		actual_json = json.loads(response.content)

		self.assertListEqual([], actual_json['matches'])
		self.assertListEqual(tables, actual_json['tables'])
		self.assertListEqual(players, actual_json['players'])
		self.assertEqual(1, actual_json['week'])
		self.assertEqual(2, actual_json['group'])

	def test_fetch_group_one_game(self):
		acdc = Table.objects.get(id=6)
		group = self.create_group(1, 1)

		players = group.players.all()
		for i, player in enumerate(players):
			self.save_game(group, player, i, acdc, i+5)

		response = self.fetch_response('api_group', group)

		actual_json = json.loads(response.content)

		self.assertEquals(200, response.status_code)
		self.assertEquals(1, len(actual_json['matches']))
		self.assertEquals(4, len(actual_json['matches'][0]['games']))
		self.assertEquals({'id': acdc.id, 'name': acdc.name}, actual_json['matches'][0]['table'])
		
		for i, player in enumerate(players):
			game = {'id': i+1, 'player': {'id': player.id, 'name': player.name}, 'league_points': i+5}
			self.assertTrue(0<=actual_json['matches'][0]['games'].index(game))

	def test_fetch_group_three_games(self):
		acdc = Table.objects.get(id=6)
		avengers = Table.objects.get(id=9)
		hook = Table.objects.get(id=1)
		group = self.create_group(1, 1)

		players = group.players.all()
		tables = [acdc, avengers, hook]
		expected_matches = [{'table': table, 'games': []} for table in tables]

		for i, player in enumerate(players):
			for table in tables:
				game = self.save_game(group, player, i, table, i+5)
				for match in expected_matches:
					if match['table'] == table:
						match['games'].append(game)

		response = self.fetch_response('api_group', group)

		actual_json = json.loads(response.content)

		self.assertEquals(200, response.status_code)
		self.assertEquals(3, len(actual_json['matches']))
		self.assertEquals(4, len(actual_json['matches'][0]['games']))
		self.assertEquals(4, len(actual_json['matches'][1]['games']))
		self.assertEquals(4, len(actual_json['matches'][2]['games']))
		
		for actual in actual_json['matches']:
			self.assertTrue('table' in actual)
			expected_match = [expected for expected in expected_matches if actual['table']['id'] == expected['table'].id][0]
			for expected_game in expected_match['games']:
				player = expected_game.player
				expected = {'id': expected_game.id, 'player': {'id': player.id, 'name': player.name}, 'league_points': expected_game.league_points}

	def create_group(self, week, group):
		group = Group(week=week, group=group)
		group.save()
		for player_id in [1,2,3,4]:
			group.players.add(Player.objects.get(id=player_id))
		return group

	def save_game(self, group, player, score, table, league_points):
		game = League_Game(player=player, group=group, table=table, score=score, league_points=league_points)
		game.save()
		return game

	def fetch_response(self, url_name, group):
		url = reverse(url_name)
		client = Client()
		return client.get('%s?week=%s&group=%s'%(url, group.week, group.group))