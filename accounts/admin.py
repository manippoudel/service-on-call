from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class AccountAdmin(UserAdmin):
	list_display = ('email','username','date_joined','contact_no', 'last_login', 'is_admin','is_staff')
	search_fields = ('email','username','contact_no')
	readonly_fields=('date_joined', 'last_login')

	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()

admin.site.register(Account,AccountAdmin)
