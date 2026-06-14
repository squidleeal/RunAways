from django.contrib import admin

from .models import Maratona


@admin.register(Maratona)
class MaratonaAdmin(admin.ModelAdmin):
	list_display = ('cidade', 'data', 'distancia')
	search_fields = ('cidade',)
	list_filter = ('cidade', 'data')
