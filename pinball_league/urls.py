from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from main import views
from main.controllers import table, player, register, login, index, week, group, setup_week, reset, rankings, divisions
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

admin.autodiscover()

class DirectTemplateView(TemplateView):
    extra_context = None
    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        if self.extra_context is not None:
            for key, value in self.extra_context.items():
                if callable(value):
                    context[key] = value()
                else:
                    context[key] = value
        return context

def main_view(path, action):
	return url(r'^%s' % (path), 'main.views.%s' % (action))

api_urls = patterns('',
	main_view('api/players', 'fetch_players'),
	main_view('api/tables', 'fetch_tables'),
    url(r'^api/setupWeek/(?P<week>.+)', setup_week.SetupWeekApiView.as_view(), name='api_setup_week'),
	url(r'^api/group', 'main.views.fetch_group', name='api_group'),
	url(r'^api/saveGame', group.SaveGamesApiView.as_view(), name='api_save_game'),
)

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^players', player.PlayersView.as_view(), name='players'),
    url(r'^player/(?P<id>.+)', player.PlayerView.as_view(), name='player'),
    url(r'^tables', table.TablesView.as_view(), name='tables'),
    url(r'^table/(?P<id>.+)', table.TableView.as_view(), name='table'),
    url(r'^register', register.SignupView.as_view(), name='register'),
    url(r'^confirmAccount/(?P<token>.+)', register.ConfirmAccountView.as_view()),
    url(r'^setupWeek', login_required(setup_week.SetupWeekView.as_view())),
    url(r'^addPlayer', login_required(register.AddPlayerView.as_view()), name='addPlayer'),
    url(r'^reset', login_required(reset.ResetView.as_view()), name='reset'),
    url(r'^login', login.LoginView.as_view(), name='login'),
    url(r'^logout', login.LogoutView.as_view(), name='logout'),
    url(r'^week/(?P<week>.+)', week.WeekView.as_view(), name='week'),
    url(r'^group', group.GroupView.as_view(), name='group'),
    url(r'^rankings', rankings.RankingsView.as_view(), name='rankings'),
    url(r'^flipOffHunger', DirectTemplateView.as_view(template_name='flip_off_hunger.html')),
    url(r'^divisions', divisions.DivisionsView.as_view(), name='divisions'),
    url(r'^$', index.IndexView.as_view(), name='home'),
)

urlpatterns = urlpatterns + api_urls + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)