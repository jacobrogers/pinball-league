from main.controllers import * 

class ResetView(BaseView):
    def get(self, request):
        League_Game.objects.all().delete()
        Ranking.objects.all().delete()
        Group.objects.all().delete()
        return redirect('/')