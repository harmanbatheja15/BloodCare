from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account

# Register your models here.

class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'blood_group', 'state', 'city', 'donate_plasma')
    list_display_links = ('email', 'name')
    readonly_fields = ('id', 'date_joined', 'last_login')
    search_fields = ('date_joined', 'phone', 'name', 'state', 'city')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)