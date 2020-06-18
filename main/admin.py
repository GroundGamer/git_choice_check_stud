from django.contrib import admin

from .models import *


# class AdvUserAdmin(admin.ModelAdmin):
#     list_display = ('__str__', 'date_joined')
#     search_fields = ('username', 'email', 'first_name', 'last_name')
#     fields = (('username', 'email'),
#               'password',
#               ('first_name', 'last_name'),
#               ('is_staff', 'is_superuser', 'is_active'),
#               'groups', 'user_permissions',
#               ('last_login', 'date_joined'))
#     readonly_fields = ('last_login', 'date_joined')


admin.site.register(HeaderModel)
admin.site.register(QuestionModel)
admin.site.register(FileDateBaseModel)
# admin.site.register(AdvUser, AdvUserAdmin)
