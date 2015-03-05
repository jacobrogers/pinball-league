from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import Client
import json

from main.models import Player, Group, League_Game

class SaveGameTestCase(TestCase):

	fixtures = ['initial_data']

	def test_save_game(self):
		url = reverse('api_save_game')
		client = Client()
		post_body = {"players":[{"id":6,"name":"Knox Harrington","score":"234"},{"id":7,"name":"Karl Hungus","score":"234"},{"id":9,"name":"Donny Kerabatsos","score":"22"},{"id":11,"name":"Jeffrey Lebowski","score":"23"}],"week":1, "group":1, "table":{"id":6,"name":"AC/DC Pro"}}
		self.initialize_data(post_body)

		response = client.post(url, content_type='application/json', data=json.dumps(post_body))

		self.assertEquals(201, response.status_code)

		games = League_Game.objects.all()
		self.assertEquals(4, len(games))
        
	def initialize_data(self, data):
		group = Group(week=data['week'], group=data['group'])
		group.save()
		for player in data['players']:
			group.players.add(Player.objects.get(id=player['id']))