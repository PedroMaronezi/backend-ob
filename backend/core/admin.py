from django.contrib import admin
from core.models import *

# Register your models here.
admin.site.register(User)
admin.site.register(MockedTransactions)
admin.site.register(MockedBankAccount)
admin.site.register(MockedConsent)
admin.site.register(Category)
admin.site.register(OBPermissions)