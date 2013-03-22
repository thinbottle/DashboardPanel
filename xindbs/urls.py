
from django.conf.urls.defaults import patterns, url
from .views import (IndexView, CreateView, UsersView, 
                    DeleteView, backup_view, restore_view, new_create_view)

urlpatterns = patterns('horizon.dashboards.syspanel.xindbs.views',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^create/$', CreateView.as_view(), name='create'),
    url(r'(?P<xindb_id>[^/]+)/backups/$', UsersView.as_view(), name="users"),
    url(r'(?P<xindb_id>[^/]+)/create_backup/$', backup_view, name="create_backup"),
    url(r'(?P<xindb_id>[^/]+)/delete_xindb/$', DeleteView.as_view(), name="delete_xindb"),
    url(r'(?P<backup_id>[^/]+)/restore_xindb/$', restore_view, name="restore_xindb"),
    url(r'(?P<xindb_id>[^/]+)/new_create/$', new_create_view, name="new_create"),
    )

