from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, PatientProfile, DoctorProfile


class CustomUserAdmin(UserAdmin):

    model = User

    list_display = (
        'email',
        'username',
        'role',
        'is_staff',
    )

    ordering = ('email',)

    fieldsets = (
        (None, {
            'fields': (
                'email',
                'username',
                'password',
                'role',
            )
        }),

        ('Permissions', {
            'fields': (
                'is_staff',
                'is_superuser',
                'is_active',
                'groups',
                'user_permissions',
            )
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'username',
                'password1',
                'password2',
                'role',
            ),
        }),
    )

    search_fields = ('email',)


admin.site.register(User,CustomUserAdmin)

admin.site.register(PatientProfile)

admin.site.register(DoctorProfile)