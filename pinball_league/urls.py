from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

def main_view(path, action):
	return url(r'^%s' % (path), 'main.views.%s' % (action))

api_urls = patterns('',
	main_view('api/players', 'fetch_players'),
	main_view('api/tables', 'fetch_tables'),
	main_view('api/saveGroups', 'save_groups'),
)

urlpatterns = patterns('',
	main_view('tables', 'tables_page'),
	main_view('players', 'players_page'),
	main_view('createGroups', 'create_groups'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'main.views.index'),
)

urlpatterns = urlpatterns + api_urls + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)