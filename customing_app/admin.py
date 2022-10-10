from django.contrib import admin

from .models import Profile, ColorScheme, Link

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ('name', 'owner')
    list_filter = tuple()


class SchemeAdmin(admin.ModelAdmin):
    model = ColorScheme
    list_display = ('owner',)
    list_filter = tuple()


admin.site.register(Profile, ProfileAdmin)
admin.site.register(ColorScheme, SchemeAdmin)