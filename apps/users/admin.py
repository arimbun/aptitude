from apps.users.models import User
from django.contrib import admin

class UserAdmin(admin.ModelAdmin):
    list_display = ('email_address', 'first_name', 'last_name', 'receive_newsletter', 'created')

admin.site.register(User, UserAdmin)

