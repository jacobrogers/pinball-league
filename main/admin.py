from django.contrib import admin

# Register your models here.
from main.models import Table, Player, League_Game, Group, Ranking

admin.site.register(Table)
admin.site.register(Player)
admin.site.register(Group)
admin.site.register(League_Game)
admin.site.register(Ranking)
