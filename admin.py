from django.contrib import admin

# Register your models here.


from .models import (
    Game,
    Player,
    Snippet
)

admin.site.register(Game)
admin.site.register(Player)
admin.site.register(Snippet)
