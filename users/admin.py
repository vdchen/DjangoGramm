from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile


# Profile Inline
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


# Custom User Admin
class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff',
                    'is_active')


# Register everything
admin.site.register(CustomUser, CustomUserAdmin)
