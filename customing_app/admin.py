from django.contrib import admin

from .models import Profile, ColorScheme, Link

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ('name', 'owner')
    list_filter = tuple()


admin.site.register(Profile, ProfileAdmin)