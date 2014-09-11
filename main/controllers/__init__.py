from main.models import Table, Player, Player_Confirmation, Group, Ranking
from django.shortcuts import render, redirect
from base import BaseView
from operator import itemgetter, attrgetter
from main.forms import SignupForm, AccountConfirmationForm
from django.http import HttpResponse
import json, datetime, os, binascii
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as django_login
from django.db.models import Max