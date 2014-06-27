from django.test import TestCase

from domain import decide_points, decide_bonus_points, create_groups

class PointSystemTestCase(TestCase):

    def test_four_player_group(self):
        scores = [4,3,2,1]

        self.assertEqual(3, decide_points(scores, 4))
        self.assertEqual(1, decide_points(scores, 2))
        self.assertEqual(2, decide_points(scores, 3))
        self.assertEqual(0, decide_points(scores, 1))

    def test_three_player_group(self):
        scores = [4,3,2]

        self.assertEqual(3, decide_points(scores, 4))
        self.assertEqual(2, decide_points(scores, 3))
        self.assertEqual(0, decide_points(scores, 2))

    def test_two_player_group(self):
        scores = [4,3]

        self.assertEqual(3, decide_points(scores, 4))
        self.assertEqual(0, decide_points(scores, 3))

    def test_two_players_bonus_point_to_second_player(self):
        scores = [9,3]

        self.assertEqual(1, decide_bonus_points(scores, 3))
        self.assertEqual(0, decide_bonus_points(scores, 9))

    def test_two_players_bonus_point_to_first_player(self):
        scores = [10,3]

        self.assertEqual(0, decide_bonus_points(scores, 3))
        self.assertEqual(1, decide_bonus_points(scores, 10))

    def test_three_players_bonus_point_to_first_player(self):
        scores = [9,5,3]

        self.assertEqual(0, decide_bonus_points(scores, 5))
        self.assertEqual(0, decide_bonus_points(scores, 3))
        self.assertEqual(1, decide_bonus_points(scores, 9))

    def test_three_players_bonus_point_to_last_player(self):
        scores = [9,6,3]

        self.assertEqual(1, decide_bonus_points(scores, 3))
        self.assertEqual(0, decide_bonus_points(scores, 6))
        self.assertEqual(0, decide_bonus_points(scores, 9))

    def test_four_players_bonus_point_to_first_player(self):
        scores = [9,3,2,1]

        self.assertEqual(1, decide_bonus_points(scores, 9))
        self.assertEqual(0, decide_bonus_points(scores, 3))
        self.assertEqual(0, decide_bonus_points(scores, 2))
        self.assertEqual(1, decide_bonus_points(scores, 1))

    def test_four_players_bonus_point_to_second_player(self):
        scores = [9,6,4,1]

        self.assertEqual(0, decide_bonus_points(scores, 9))
        self.assertEqual(1, decide_bonus_points(scores, 6))
        self.assertEqual(1, decide_bonus_points(scores, 4))
        self.assertEqual(0, decide_bonus_points(scores, 1))
    
    def test_four_players_bonus_point_to_third_player(self):
        scores = [9,6,4,3]

        self.assertEqual(0, decide_bonus_points(scores, 9))
        self.assertEqual(0, decide_bonus_points(scores, 6))
        self.assertEqual(1, decide_bonus_points(scores, 4))
        self.assertEqual(1, decide_bonus_points(scores, 3))

class SetupWeekTestCase(TestCase):

    def test_create_groups_of_four(self):
        players = [{'rank': rank} for rank in range(1,9)]

        groups = create_groups(players)

        self.assertEqual(2, len(groups))

        for group in groups: 
            self.assertEqual(4, len(group['players']))
