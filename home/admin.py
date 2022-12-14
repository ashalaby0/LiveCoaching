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
    pass


@admin.register(models.Category)
class CategoryModelAdmin(admin.ModelAdmin):
    pass
