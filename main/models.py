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
	tutorial = models.URLField(null=True,blank=True)

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
	status = models.CharField(max_length=10,choices=( ('Active','Active'), ('Inactive', 'Inactive')), default='Active')
	created = models.DateField(default=datetime.date.today)
	week_points = 0
	
	@property
	def name(self):
		return '%s %s' % (self.first_name.capitalize(), self.last_name.capitalize())

	@property
	def total_points(self):
		return sum([game.league_points for game in self.games.all()])

	@property
	def total_bonus_points(self):
		return sum([game.bonus_points for game in self.games.all()])

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
	players = models.ManyToManyField(Player, related_name="groups")
	created = models.DateField(default=datetime.date.today)

	@property
	def is_open(self):
		for game in self.games.all():
			if game.score == None:
				return True
		return False

	def as_json(self):
		return dict(week=self.week, group=self.group, games=self.games)
		
	def __unicode__(self):
		return 'Week %s Group %s' % (self.week,self.group)

	class Meta:
		db_table = 'groups'

class League_Game(models.Model):
	player = models.ForeignKey(Player, related_name="games")
	table = models.ForeignKey(Table, related_name="games", null=True, blank=True)
	group = models.ForeignKey(Group, related_name="games")
	score = models.BigIntegerField(null=True,blank=True)
	league_points = models.IntegerField(null=True,blank=True,default=0)
	is_pre_play = models.BooleanField(default=False)
	is_post_play = models.BooleanField(default=False)
	created = models.DateField(default=datetime.date.today)

	def __unicode__(self):
		return 'Week %s Group %s: %s %s' % (self.group.week, self.group.group, self.player.name, self.table.name)

	class Meta:
		db_table = 'league_games'

class Ranking(models.Model):
	week = models.IntegerField()
	player = models.ForeignKey(Player, related_name="rankings")
	rank = models.IntegerField()
	points = models.IntegerField(default=0)
	created = models.DateField(default=datetime.date.today)

	def __unicode__(self):
		return 'Week %s Player %s Rank %s' % (self.week, self.player.name, self.rank)

	class Meta:
		db_table = 'rankings'