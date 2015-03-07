from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import Client
import json

from main.models import Player, Group, League_Game

class SaveGameTestCase(TestCase):

	fixtures = ['initial_data']

	def test_save_game_no_existing_games(self):
		url = reverse('api_save_game')
		client = Client()
		post_body = {"players":[{"id":6,"name":"Knox Harrington","score":"234"},{"id":7,"name":"Karl Hungus","score":"234"},{"id":9,"name":"Donny Kerabatsos","score":"22"},{"id":11,"name":"Jeffrey Lebowski","score":"23"}],"week":1, "group":1, "table":{"id":6,"name":"AC/DC Pro"}}
		self.initialize_data(post_body)

		response = client.post(url, content_type='application/json', data=json.dumps(post_body))

		self.assertEquals(201, response.status_code)

		games = League_Game.objects.all()
		self.assertEquals(4, len(games))

		json_response = json.loads(response.content)
		self.assertEquals(4, len(json_response))

		for player in post_body['players']:
			for game in json_response:
				self.assertTrue(0<game['id'])
				if game['player'] == player['id']:
					self.assertEquals(player['score'], game['score'])
					self.assertEquals(post_body['table']['id'], game['table'])

	def test_update_game(self):
		url = reverse('api_save_game')
		client = Client()
		post_body = {"players":[{"id":6,"name":"Knox Harrington","score":"234"},{"id":7,"name":"Karl Hungus","score":"234"},{"id":9,"name":"Donny Kerabatsos","score":"22"},{"id":11,"name":"Jeffrey Lebowski","score":"23"}],"week":1, "group":1, "table":{"id":6,"name":"AC/DC Pro"}}
		self.initialize_data(post_body)

		response = client.post(url, content_type='application/json', data=json.dumps(post_body))

		games = League_Game.objects.all()
		self.assertEquals(4, len(games))

		update_post_body = {"players":[{"id":6,"name":"Knox Harrington","score":"987"},{"id":7,"name":"Karl Hungus","score":"3884"},{"id":9,"name":"Donny Kerabatsos","score":"38"},{"id":11,"name":"Jeffrey Lebowski","score":"34883"}],"week":1, "group":1, "table":{"id":5,"name":"AC/DC Pro"}}
		response = client.post(url, content_type='application/json', data=json.dumps(update_post_body))

		games = League_Game.objects.all()
		self.assertEquals(4, len(games))		
		
		json_response = json.loads(response.content)
		for player in update_post_body['players']:
			for game in json_response:
				self.assertTrue(0<game['id'])
				if game['player'] == player['id']:
					self.assertEquals(player['score'], game['score'])
					self.assertEquals(update_post_body['table']['id'], game['table'])

        
	def initialize_data(self, data):
		group = Group(week=data['week'], group=data['group'])
		group.save()
		for player in data['players']:
			group.players.add(Player.objects.get(id=player['id']))