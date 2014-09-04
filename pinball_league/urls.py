from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from main import views
admin.autodiscover()

def main_view(path, action):
	return url(r'^%s' % (path), 'main.views.%s' % (action))

api_urls = patterns('',
	# main_view('api/players', 'fetch_players'),
	# main_view('api/tables', 'fetch_tables'),
	main_view('api/saveGroups', 'save_groups'),
	main_view('api/week/(?P<week>.+)', 'fetch_groups'),
    main_view('api/setupWeek/(?P<week>.+)', 'setup_week'),
	main_view('api/group', 'fetch_group'),
	main_view('api/saveGames', 'save_games'),
    main_view('api/overview', 'overview'),
    main_view('api/signup', 'signup'),
    main_view('api/lookupConfirmation/(?P<token>.+)', 'fetch_player_confirmation'),
    main_view('api/confirm_account/(?P<token>.+)', 'confirm_account'),
)

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tables', views.TableView.as_view()),
    url(r'^players', views.PlayerView.as_view()),
    url(r'^api/auth/$', views.AuthView.as_view(), name='authenticate'),
    url(r'^$', 'main.views.index'),
)

urlpatterns = urlpatterns + api_urls + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)