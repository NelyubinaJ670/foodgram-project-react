from django.contrib.auth import get_user_model
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

User = get_user_model()


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('id', 'first_name', 'last_name', 'email',)
    search_fields = ('email', 'first_name',)
    list_filter = ('email', 'first_name',)


admin.site.register(User, CustomUserAdmin)
