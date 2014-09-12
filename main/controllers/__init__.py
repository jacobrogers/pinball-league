from django.views.generic import View
from django.shortcuts import render, redirect
from operator import itemgetter, attrgetter
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as django_login
from django.db.models import Max, Sum
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import json, datetime, os, binascii
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator

from main.models import Table, Player, Player_Confirmation, Group, Ranking, League_Game
from main.util import send_email, json_response, basic_json
from main.domain import group_players, decide_points, decide_bonus_points
from main.forms import SignupForm, AccountConfirmationForm
from base import BaseView