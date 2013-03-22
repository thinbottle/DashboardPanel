import logging

from django.utils.translation import ugettext_lazy as _
from django.core import urlresolvers

from horizon import api
from horizon import tables

from ..users.tables import UsersTable


LOG = logging.getLogger(__name__)

class CreateXindb(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Xindb")
    url = "horizon:syspanel:xindbs:create"
    classes = ("ajax-modal","btn-create")
    #classes = ("btn-create",)

class ViewBackupLink(tables.LinkAction):
    name = "xindb-backups"
    verbose_name = _("View Backup")
    url = "horizon:syspanel:xindbs:users"
    classes = ("btn-download",)

class CreateBackup(tables.LinkAction):
    name = "create backup"
    verbose_name = _("Create Backup")
    url = "horizon:syspanel:xindbs:create_backup"
    #classes = ("ajax-modal", "btn-create")
    classes = ("btn-download",)

class DeleteXindb(tables.LinkAction):
    name = "delete xindb"
    verbose_name = _("Delele Xindb")
    url = "horizon:syspanel:xindbs:delete_xindb"
    classes = ("btn-download")

class RestoreBackup(tables.LinkAction):
    name = "restore"
    verbose_name = _("Restore xindb")
    url = "horizon:syspanel:xindbs:restore_xindb"
    classes = ("btn-download")

class NewCreate(tables.LinkAction):
    name = "new create"
    verbose_name = ("New Create")
    url = "horizon:syspanel:xindbs:new_create"
    classes = ("btn-download",)
    

    
class XindbsTable(tables.DataTable):
    xindb_id = tables.Column('id', verbose_name=_('ID'))
    name = tables.Column('name', verbose_name=_('Xindb Name'))
    state = tables.Column('state', verbose_name=_('State'))
    db_type = tables.Column('db_type', verbose_name=_('DB Type'))
    ha = tables.Column('ha', verbose_name=_('HA'))

    class Meta:
        name = "xindbs"
        verbose_name = _("Xindbs")
        table_actions = (CreateXindb,) #DeleteXindb,)
        row_actions = (ViewBackupLink, CreateBackup, DeleteXindb)
    
class BackupsTable(tables.DataTable):
    backups = tables.Column('backup', verbose_name=_('Backup'))
    size = tables.Column('size', verbose_name=_('size'))

    class Meta:
        name = "xindb_backups"
        verbose_name = _("Xindb_backups")
        #table_actions = (CreateBackup,)
        table_actions = (NewCreate,)
        row_actions = (RestoreBackup,)
