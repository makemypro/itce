from django.contrib import admin
from .models import Technology


# Register your models here.
@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon')
