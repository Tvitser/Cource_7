from django.contrib import admin

# Register your models here.
from core.models import User


class AuthorAdmin(admin.ModelAdmin):
    exclude = ('password', 'permissions', 'groups')
    search_fields = ['username', 'first_name', 'last_name', 'email']
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    readonly_fields = ("last_login", "date_joined")

admin.site.register(User, AuthorAdmin)