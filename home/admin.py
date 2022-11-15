from django.contrib import admin

# Register your models here.
from . import models

@admin.register(models.Coach)
class CoachModelAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Client)
class ClientModelAdmin(admin.ModelAdmin):
    pass