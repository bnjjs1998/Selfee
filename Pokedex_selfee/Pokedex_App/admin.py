from django.contrib import admin

from .models import ModelType_pokemon

@admin.register(ModelType_pokemon)
class ModelTypePokemonAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "types_pokemon", "date_creation")
    search_fields = ("user__username", "types_pokemon")
    list_filter = ("types_pokemon", "date_creation")