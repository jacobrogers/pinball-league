from main.controllers import *

class GroupView(BaseView):
    template = 'group.html'

    def doGet(self, request):
        (week, group) = (request.GET.get('week'), request.GET.get('group'))
        canEnterScores = self.user_can_enter_scores(request.user, week, group) if request.user.is_authenticated() else False
        return {'week': week, 'group': group, 'canEnterScores': canEnterScores}

class SaveGamesApiView(BaseView):

    def post(self, request):
        payload = json.loads(request.POST.dict().keys()[0])
        games = payload['games']
        scores = sorted([game['score'] for game in games],reverse=True)
        points = []
        for game in games:
            savedGame = League_Game.objects.get(id=game['id'])
            savedGame.score = game['score']
            savedGame.league_points = decide_points(scores, savedGame.score)
            savedGame.bonus_points = decide_bonus_points(scores, savedGame.score)
            points.append({'id': game['id'], 'league_points': savedGame.league_points, 'bonus_points': savedGame.bonus_points})
            savedGame.save()
        return json_response(points, 201)