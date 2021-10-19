from django.contrib import admin
from Contacts.models import Contacts, Company
from TradeManagementBackend.GuardedModelAdminBase import GuardedModelAdminEx

# Register your models here.

class ContactsAdmin(GuardedModelAdminEx):
    pass

class CompanyAdmin(GuardedModelAdminEx):
    pass

admin.site.register(Contacts, ContactsAdmin)
admin.site.register(Company, CompanyAdmin)
