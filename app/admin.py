from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Band, Guy, Alert, AlertLog


class GuyInline(admin.StackedInline):
    model = Guy
    can_delete = False
    verbose_name_plural = 'guy'

class UserAdmin(UserAdmin):
    inlines = (GuyInline, )


admin.site.register(Band)
admin.site.register(Alert)
admin.site.register(AlertLog)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
