from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User, Subscription
from users.models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('id', 'first_name', 'last_name', 'email',)
    search_fields = ('email', 'first_name',)
    list_filter = ('email', 'first_name',)


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'author', 'date_added',)


admin.site.register(User, CustomUserAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
