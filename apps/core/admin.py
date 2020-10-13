from django.contrib import admin

from django.contrib.auth.models import User, Group

# Register your models here.

#admin.site.unregister(User)
admin.site.unregister(Group)

admin.site.site_header = 'Grade Horária - Login'
admin.site.site_title = 'Administração Grade Horária'
admin.site.index_title = 'Administração Grade Horária - Aplicações'