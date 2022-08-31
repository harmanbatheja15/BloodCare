from django.contrib import admin
from .models import Contact, State, City, BloodBank
from import_export.admin import ImportExportModelAdmin

# Register your models here.

class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone', 'message')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name', 'email', 'message')
    list_per_page = 25

class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'state', 'state_id')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')
    list_per_page = 100

class StateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')
    list_per_page = 100

class BloodBankAdmin(ImportExportModelAdmin):
    list_display = ('id', 'Blood_Bank_Name', 'States', 'City', 'Address', 'Contact_No')
    list_display_links = ('id', 'Blood_Bank_Name')
    search_fields = ('id', 'States', 'City')

admin.site.register(Contact, ContactAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(BloodBank, BloodBankAdmin)