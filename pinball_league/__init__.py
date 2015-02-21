import os
from os.path import join

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def is_local_development():
	return 'DJANGO_DEBUG' in os.environ