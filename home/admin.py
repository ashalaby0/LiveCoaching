from django.contrib import admin

# Register your models here.
from home import models


@admin.register(models.Coach)
class CoachModelAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Client)
class ClientModelAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Session)
class SessionModelAdmin(admin.ModelAdmin):
    list_display = ['coach', 'group_session', 'time', 'duration']


@admin.register(models.Category)
class CategoryModelAdmin(admin.ModelAdmin):
    pass


@admin.register(models.CustomerMessage)
class CustomerMessageModelAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ZoomMeeting)
class ZoomMeetingModelAdmin(admin.ModelAdmin):
    pass