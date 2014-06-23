from django.db import models

class Table(models.Model):
	name = models.CharField(max_length=50)
	ipdb_id = models.IntegerField()
	pinside_name = models.CharField(max_length=50)
	status = models.CharField(max_length=10,choices=( ('Active','Active'), ('Inactive', 'Inactive')), default='Active')

	def __unicode__(self):
		return self.name

	class Meta:
		db_table = 'tables'

class Player(models.Model):
	name = models.CharField(max_length=100)
	ifpa_id = models.IntegerField(null=True,blank=True)
	signature = models.CharField(max_length=3,null=True,blank=True)

	def __unicode__(self):
		return '%s [%s]' % (self.name, self.signature)

	class Meta:
		db_table = 'players'

class Group(models.Model):
	week = models.IntegerField()
	group = models.IntegerField()

	def as_json(self):
		return dict(week=self.week, group=self.group, games=self.games)
		
	def __unicode__(self):
		return 'Week %i Group %i' % (self.week,self.group)

	class Meta:
		db_table = 'groups'

class League_Game(models.Model):
	player = models.ForeignKey(Player)
	table = models.ForeignKey(Table)
	group = models.ForeignKey(Group, related_name="games")
	order = models.IntegerField(max_length=1,null=True,blank=True)
	score = models.IntegerField(null=True,blank=True)
	league_points = models.IntegerField(null=True,blank=True)
	bonus_points = models.IntegerField(null=True,blank=True)

	def __unicode__(self):
		return 'Week %i Group %i: %s %s' % (self.group.week, self.group.group, self.player.name, self.table.name)

	class Meta:
		db_table = 'league_games'

class Ranking(models.Model):
	week = models.IntegerField()
	player = models.ForeignKey(Player)
	rank = models.IntegerField()
	points = models.IntegerField(default=0)

	def __unicode__(self):
		return 'Week %i Player %s Rank %i' % (self.week, self.player.name, self.rank)

	class Meta:
		db_table = 'rankings'