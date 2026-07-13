from django.db import models
from django.conf import settings

class ModelType_pokemon(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="mes_models",
    )

    
    types_pokemon = models.CharField(max_length=100)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Type Pokémon"
        verbose_name_plural = "Types Pokémon"

    def __str__(self):
        return self.types_pokemon