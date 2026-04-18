from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account


class AccountAdmin(UserAdmin):
    list_display  = ('email', 'first_name', 'last_name', 'username', 'is_active')
    list_filter   = ('is_admin', 'is_staff', 'is_active')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering      = ('email',)

    
    filter_horizontal  = ()
    fieldsets          = ()
    list_filter        = ()


admin.site.register(Account, AccountAdmin)