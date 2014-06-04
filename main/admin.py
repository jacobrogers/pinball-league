from django.contrib import admin

# Register your models here.
from main.models import League_Season, Table, Player, League_Game, Group

admin.site.register(League_Season)
admin.site.register(Table)
admin.site.register(Player)
admin.site.register(Group)
admin.site.register(League_Game)
