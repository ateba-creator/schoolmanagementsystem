from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from accounts.models import Teacher
# Register your models here.

from django.contrib import admin


class CustomUserAdmin(UserAdmin):
    """Define admin model for custom User model with no username field."""
    fieldsets = (
        (None, {'fields': ('phone_no', 'password')}),
        (_('Personal info'), {'fields': (
            'department',
            'last_name',
            'first_name',
            'email',
            'date_of_birth',
            'place_of_birth',
            'gender',
            'address',
            'classrooms',
            'is_authorized',
        )}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups',)}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_no', 'password1', 'password2'),
        }),
    )
    list_display = ( 'phone_no','first_name','last_name','email', 'is_staff')
    search_fields = ( 'first_name', 'last_name','phone_no')
    ordering = ('first_name',)


admin.site.register(Teacher , CustomUserAdmin)