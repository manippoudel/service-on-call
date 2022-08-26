from django.contrib import admin
from .models import(
    about_member,
    home_page,
    Review,
    Service_Provider,
)

#this is the block use to customize the view of the data entered in the database.
#we have to pass models with the new models created in order to make it visible
class SP_Admin(admin.ModelAdmin):
    list_display    = ('name', 'is_approved', 'date_joined', 'location', 'contactno', 'panno' )
    readonly_fields = ('date_joined','slug')
    search_fields = ('panno','contact_no')
    filter_horizontal = ()
    list_filter = ('date_joined',)
    fieldsets = ()
    date_hierarchy = 'date_joined'
    actions = ['Approve',]

    def Approve(self, request, queryset):
        queryset.update(is_approved=True)


admin.site.register(Service_Provider,SP_Admin)
admin.site.register(home_page)
admin.site.register(about_member)
admin.site.register(Review)

# admin.site.site_header = 'Service On Call'