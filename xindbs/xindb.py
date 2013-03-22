

from nova import novaclient

def xindb_list(request):
    return novaclient(request).xindbs.list()

def xindb_get(request, xindb_id):
    return novaclient(request).xindbs.get(xindb_id)

def xindb_delete(request, xindb_id):
    novaclient(request).xindbs.delete(xindb_id)

def xindb_create(request, name, flavor, db_type=False, ha=False, **kwargs):
    return novaclient(request).xindbs.create(name, flavor, db_type, ha, **kwargs)

def xindb_backup_create(request,xindb_id):
    return novaclient(request).xindbs.backup_create(xindb_id)

def xindb_backup_list(request, xindb_id):
    return novaclient(request).xindbs.backup_list(xindb_id)

def xindb_restore(request, xindb_id, backup_id):
    LOG.error("in xindb_restore")
    return novaclient(request).xindbs.backup_restore(xindb_id, backup_id)

