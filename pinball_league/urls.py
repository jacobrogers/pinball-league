from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from main import views
admin.autodiscover()

def main_view(path, action):
	return url(r'^%s' % (path), 'main.views.%s' % (action))

api_urls = patterns('',
	main_view('api/players', 'fetch_players'),
	main_view('api/tables', 'fetch_tables'),
	main_view('api/saveGroups', 'save_groups'),
    main_view('api/setupWeek/(?P<week>.+)', 'setup_week'),
	main_view('api/saveGames', 'save_games'),
)

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tables', views.TableView.as_view(), name='tables'),
    url(r'^players', views.PlayerView.as_view(), name='players'),
    url(r'^register', views.SignupView.as_view(), name='register'),
    url(r'^confirmAccount/(?P<token>.+)', views.ConfirmAccountView.as_view()),
    url(r'^setupWeek', views.SetupWeekView.as_view()),
    url(r'^week/(?P<week>.+)', views.WeekView.as_view()),
    url(r'^login', views.LoginView.as_view(), name='login'),
    url(r'^logout', views.LogoutView.as_view(), name='logout'),
    url(r'^week/(?P<week>.+)/group/(?P<group>.+)', views.GroupView.as_view(), name='group'),
    url(r'^week/(?P<week>.+)', views.WeekView.as_view(), name='week'),
    url(r'^$', views.IndexView.as_view(), name='home'),
)

urlpatterns = urlpatterns + api_urls + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)