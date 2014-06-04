from django.db import models

class League_Season(models.Model):
	start_date = models.DateField()
	weeks = models.IntegerField()
	
	def __unicode__(self):
		return '%s %s' % (self.start_date, self.weeks)

	class Meta:
		db_table = 'seasons'

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