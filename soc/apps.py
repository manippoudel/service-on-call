from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class SocConfig(AppConfig):
    name = 'soc'
    verbose_name 	= _('Service On Call')
#to change the app name in the admin view in the site
#there can be multiple mthod to change it
#as you can add appname.apps.AppnameConfig in installed app section