from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CUserChangeForm, UserRegistrationForm
from .models import User

# Register your models here.
class CustomUserAdmin(UserAdmin):
    add_form = UserRegistrationForm
    form = CUserChangeForm
    model = User
    list_display = ('username', 'email', 'is_staff', 'is_active',)
    list_filter = ('is_staff', 'is_active',)
    fieldsets = (
        ('Base information', {'fields': ('username', 'email', 'password',)}),
        ('Permissions', {'fields': ('user_permissions', 'is_staff', 'is_active', 'date_joined',)}),
        ('Secrets', {'fields': ('user_token',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password', 'password2',)}
        ),
    )
    search_fields = ('username',)
    ordering = ('is_staff', 'is_active',)


admin.site.register(User, CustomUserAdmin)