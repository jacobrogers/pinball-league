from main.controllers import BaseView, Player, Group, League_Game, render, Max, Sum, basic_json, group_players, json_response

class SetupWeekApiView(BaseView):
    def get(self,request, week):
        players = League_Game.objects.filter(group__week=int(week)-1).values('group__group', 'player').annotate(points=Sum('league_points', field='league_points+bonus_points'))
        groups = {group+1: [] for group in range(len({player['group__group'] for player in players}))}
        for player in players:
            real_player = Player.objects.get(id=player['player'])
            groups[player['group__group']].append({'name': real_player.name, 'id': real_player.id, 'league_points': player['points']})
        new_players = [basic_json(player) for player in Player.objects.all() if not self.player_has_game(players, player)]
        model = {'groups': group_players(groups), 'players': new_players}
        return json_response(model)

    def player_has_game(self,players, player):
        for p in players:
            if p['player'] == player.id:
                return True
        return False