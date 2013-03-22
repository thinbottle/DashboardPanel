
from django.utils.translation import ugettext_lazy as _

import horizon
from horizon.dashboards.syspanel import dashboard

class Xindbs(horizon.Panel):
    name = _("Xindbs")
    slug = 'xindbs'

dashboard.Syspanel.register(Xindbs)
    
