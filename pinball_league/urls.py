from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from main import views
from main.controllers import table, player, register, login, index, week, group
admin.autodiscover()

def main_view(path, action):
	return url(r'^%s' % (path), 'main.views.%s' % (action))

api_urls = patterns('',
	main_view('api/players', 'fetch_players'),
	main_view('api/tables', 'fetch_tables'),
	main_view('api/saveGroups', 'save_groups'),
    main_view('api/setupWeek/(?P<week>.+)', 'setup_week'),
	main_view('api/group', 'fetch_group'),
	main_view('api/saveGames', 'save_games'),
)

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^players', player.PlayersView.as_view(), name='players'),
    url(r'^player/(?P<id>.+)', player.PlayerView.as_view(), name='player'),
    url(r'^tables', table.TablesView.as_view(), name='tables'),
    url(r'^table/(?P<id>.+)', table.TableView.as_view(), name='table'),
    url(r'^register', register.SignupView.as_view(), name='register'),
    url(r'^confirmAccount/(?P<token>.+)', register.ConfirmAccountView.as_view()),
    url(r'^setupWeek', week.SetupWeekView.as_view()),
    url(r'^login', login.LoginView.as_view(), name='login'),
    url(r'^logout', login.LogoutView.as_view(), name='logout'),
    url(r'^week/(?P<week>.+)', week.WeekView.as_view(), name='week'),
    url(r'^group', group.GroupView.as_view(), name='week'),
    url(r'^$', index.IndexView.as_view(), name='home'),
)

urlpatterns = urlpatterns + api_urls + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)