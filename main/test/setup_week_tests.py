from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import Client
import json
import django

from main.models import Player, Ranking

class SetupWeekTestCase(TestCase):

	fixtures = ['initial_data']

	def test_save_week(self):
		url = reverse('api_setup_week', kwargs={'week': 1})
		client = Client()
		post_body = {"groups":[{"players":[{"id":6,"name":"Knox Harrington","rank":1},{"id":7,"name":"Karl Hungus","rank":2},{"id":12,"name":"Uli Kunkel","rank":3},{"id":9,"name":"Donny Kerabatsos","rank":4}]}]}

		response = client.post(url, content_type='application/json', data=json.dumps(post_body))

		self.assertEquals(201, response.status_code)

		player1 = Player.objects.get(id=6)
		ranking1 = Ranking.objects.get(player=player1)
		self.assertEquals(1, ranking1.rank)
        