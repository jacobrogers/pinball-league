from django.db import models
from django.contrib.auth.models import User
import datetime

class Table(models.Model):
	name = models.CharField(max_length=50)
	ipdb_id = models.IntegerField()
	pinside_name = models.CharField(max_length=50)
	status = models.CharField(max_length=10,choices=( ('Active','Active'), ('Inactive', 'Inactive')), default='Active')
	created = models.DateField(default=datetime.date.today)
	image = models.URLField()

	def __unicode__(self):
		return self.name

	class Meta:
		db_table = 'tables'
		ordering = ['name']

class Player(models.Model):
	ifpa_id = models.IntegerField(null=True,blank=True)
	signature = models.CharField(max_length=3,null=True,blank=True)
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	user = models.ForeignKey(User,null=True)
	created = models.DateField(default=datetime.date.today)

	@property
	def name(self):
		return '%s %s' % (self.first_name.capitalize(), self.last_name.capitalize())
		
	def __unicode__(self):
		return self.name

	class Meta:
		db_table = 'players'
		ordering = ['last_name']

class Player_Confirmation(models.Model):
	username = models.CharField(max_length=50,unique=True)
	email = models.EmailField()
	confirmation_token = models.CharField(max_length=50)
	created = models.DateField(default=datetime.date.today)

	class Meta:
		db_table = 'account_confirmations'

class Group(models.Model):
	week = models.IntegerField()
	group = models.IntegerField()
	created = models.DateField(default=datetime.date.today)

	def as_json(self):
		return dict(week=self.week, group=self.group, games=self.games)
		
	def __unicode__(self):
		return 'Week %i Group %i' % (self.week,self.group)

	class Meta:
		db_table = 'groups'

class League_Game(models.Model):
	player = models.ForeignKey(Player, related_name="games")
	table = models.ForeignKey(Table, related_name="games")
	group = models.ForeignKey(Group, related_name="games")
	order = models.IntegerField(max_length=1,null=True,blank=True)
	score = models.IntegerField(null=True,blank=True)
	league_points = models.IntegerField(null=True,blank=True)
	bonus_points = models.IntegerField(null=True,blank=True)
	created = models.DateField(default=datetime.date.today)

	def __unicode__(self):
		return 'Week %i Group %i: %s %s' % (self.group.week, self.group.group, self.player.name, self.table.name)

	class Meta:
		db_table = 'league_games'

class Ranking(models.Model):
	week = models.IntegerField()
	player = models.ForeignKey(Player)
	rank = models.IntegerField()
	points = models.IntegerField(default=0)
	created = models.DateField(default=datetime.date.today)

	def __unicode__(self):
		return 'Week %i Player %s Rank %i' % (self.week, self.player.name, self.rank)

	class Meta:
		db_table = 'rankings'