from django.contrib import admin

from .models import Profile, ColorScheme, Link

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ('name', 'owner')
    list_filter = tuple()


class SchemeAdmin(admin.ModelAdmin):
    model = ColorScheme
    list_filter = tuple()


class LinksAdmin(admin.ModelAdmin):
    model = Link
    list_display = ('title', 'user_profile', 'icon',)
    list_filter = ('icon', 'user_profile',)


admin.site.register(Profile, ProfileAdmin)
admin.site.register(ColorScheme, SchemeAdmin)
admin.site.register(Link, LinksAdmin)