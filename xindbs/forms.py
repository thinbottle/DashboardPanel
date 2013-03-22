
import logging

from django import shortcuts
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from horizon import api
from horizon import forms


LOG = logging.getLogger(__name__)


class CreateXindb(forms.SelfHandlingForm):
    #xindb_id = forms.IntegerField(label=_("Xindb ID"))
    name = forms.CharField(max_length="25", label=_("Name"))
    flavor = forms.CharField(max_length="25", label=_("Flavor"))
    db_type = forms.CharField(max_length="10", label=_("DB Type"))
    ha = forms.CharField(max_length="10", label=_("HA"))
    LOG.error("------------------>1")
    def _get_new_xindb_id(self):
        LOG.error("------------>2")
        xindbs = []
        xindbs = api.xindb_list(self.request)
        if xindbs:
            largest_id = max(xindbs, key=lambda x: x.id).id
            xindb_id = int(largest_id) + 1
        else:
            xindb_id = 1
        
        return xindb_id
        

    def handle(self, request, data):
        LOG.error("------------------>3")
        xindb = api.xindb_create(request,
                                 data['name'],
                                 data['flavor'],
                                 data['db_type'],
                                 data['ha'],
                                 xindb_id=self._get_new_xindb_id(),
                                  )
        msg = _("%s was successfully added to xindbs.") % data['name']
        LOG.info(msg)
        messages.success(request, msg)
        return xindb
        #return shortcuts.redirect('horizon:syspanel:xindbs:index')

class CreateBackup(forms.SelfHandlingForm):
    #NoReverseMatch: Reverse for 'create_backup' with arguments '()' and keyword arguments '{}' not found.    
    LOG.error("IN CreateXindb()")
    def _get_current_xindb_id(self):
        LOG.error("IN CreateXindb _get_current_xindb_id()")
        LOG.error("%r" % self.request.path.split("/"))
        return self.request.path.split("/")[-3]

    def handle(self, request, data):
        LOG.error("IN CreateXindb handle()")
        LOG.error("%r" % data)
        xindb_id = self._get_current_xindb_id()
        args = ["test", "n_args"]
        kwargs = {"a" : "1", "b": "3"}
        
        backup = api.xindb_backup_create(self.request, xindb_id, args=args, kwargs=kwargs)
        return backup

        
