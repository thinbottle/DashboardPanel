
import logging

from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _ 
from novaclient import exceptions as api_exceptions

from horizon import api
from horizon import forms
from horizon import tables
from .tables import XindbsTable, BackupsTable #TenantUsersTable
from .forms import CreateXindb, CreateBackup

from django.http import HttpResponseRedirect, HttpResponse

LOG = logging.getLogger(__name__)

class IndexView(tables.DataTableView):  
    table_class = XindbsTable
    template_name = 'syspanel/flavors/index.html'

    def get_data(self):
        request = self.request
        xindbs = []
        try:
            xindbs = api.xindb_list(request)
        except api_exceptions.Unauthorized, e:
            LOG.exception('Unauthorized attempt to access xindb list.')
            messages.error(request, _('Unauthorized.'))
        except Exception, e:
            LOG.exception('Exception while fetching usage info')
            if not hasattr(e, 'message'):
                e.message = str(e)
            messages.error(request, _('Unable to get xindb list: %s') % 
                            e.message) 
        xindbs.sort(key=lambda x: x.id, reverse=False)
        return xindbs

class UsersView(tables.DataTableView):
    table_class = BackupsTable
    template_name = "syspanel/xindbs/index.html"
    
    def _get_xindb_id(self):
        return self.request.path.split("/")[-3]

    def _handle_xindbs(self):
        LOG.error("UsersView: request = %r" %  self.request)
        xindb_id =self._get_xindb_id()
        try:
            xindbs = api.xindb_backup_list(self.request, xindb_id)
        except api_exceptions.Unauthorized, e:
            LOG.exception('Unauthorized attempt to access xindb buckup list.')
            messages.error(request, _('Unauthorized.'))
        except Exception, e:
            LOG.exception('Exception while fetching usage info')
            if not hasattr(e, 'message'):
                e.message = str(e)
            messages.error(request, _('Unable to get xindb backup list: %s') % 
                            e.message) 
        for i in xindbs:
            i.id = i.backup
        return xindbs

    def get_data(self):
        return self._handle_xindbs()

def backup_view(request, xindb_id):
    LOG.error("IN backup_view()")
    xindb_id = xindb_id
    try:
        backup = api.xindb_backup_create(request, xindb_id)
    except api_exceptions.Unauthorized, e:
        LOG.exception('Unauthorized attempt to access xindb buckup create.')
        messages.error(request, _('Unauthorized.'))
    except Exception, e:
        LOG.exception('Exception while fetching usage info')
        if not hasattr(e, 'message'):
            e.message = str(e)
        messages.error(request, _('Unable to get xindb backup create: %s') % 
                        e.message) 
    LOG.error("%r" % backup)
    msg = ("xindb_id: %s; %s") % (xindb_id, backup)
    messages.success(request, msg)
    return HttpResponseRedirect("http://10.12.30.11/horizon/syspanel/xindbs/%s/backups" % 
                                    xindb_id)

def new_create_view(request, xindb_id):
    LOG.error("IN new_create_view()")
    xindb_id = xindb_id
    backup = api.xindb_backup_create(request, xindb_id)
    msg = ("xindb_id: %s is creating backup: %s") % (xindb_id, backup)
    messages.success(request, msg)
    return HttpResponseRedirect("http://10.12.30.11/horizon/syspanel/xindbs/%s/backups" % 
                                    xindb_id)
    

def restore_view(request, backup_id):
    backup_id = backup_id
    referer = request.META.get("HTTP_REFERER")
    xindb_id = referer.split("/")[-3]
    try:
        ret = api.xindb_restore(request, xindb_id, backup_id)
    except api_exceptions.Unauthorized, e:
        LOG.exception('Unauthorized attempt to access xindb buckup restore.')
        messages.error(request, _('Unauthorized.'))
    except Exception, e:
        LOG.exception('Exception while fetching usage info')
        if not hasattr(e, 'message'):
            e.message = str(e)
        messages.error(request, _('Unable to get xindb backup restore: %s') % 
                        e.message) 
    status = ret[0].get("status")
    msg = ("xindb_id: %s; backup_id: %s; restore status: %s") % (
                    xindb_id, backup_id, status)
    messages.success(request, msg)
    return HttpResponseRedirect("http://10.12.30.11/horizon/syspanel/xindbs/%s/backups" % 
                                    xindb_id)

class CreateView(forms.ModalFormView):
    form_class = CreateXindb 
    template_name = 'syspanel/xindbs/create.html'
    success_url = reverse_lazy("horizon:syspanel:xindbs:index")

class DeleteView(IndexView):

    def _get_xindb_id(self):
        return int(self.request.path.split("/")[-3])

    def get_data(self):
        request = self.request
        xindb_id = self._get_xindb_id()
        try:
            xindbs = api.xindb_list(request)
        except api_exceptions.Unauthorized, e:
            LOG.exception('Unauthorized attempt to access xindb buckup restore.')
            messages.error(request, _('Unauthorized.'))
        except Exception, e:
            LOG.exception('Exception while fetching usage info')
            if not hasattr(e, 'message'):
                e.message = str(e)
            messages.error(request, _('Unable to get xindb backup restore: %s') % 
                        e.message) 
        for xindb in xindbs:
            if self.table.get_object_id(xindb) == xindb_id:
                api.xindb_delete(request, xindb)
                xindbs.remove(xindb) 
                msg = _("%s was successfully deleted from xindbs.") % xindb
                messages.success(request, msg)
        return xindbs
        

