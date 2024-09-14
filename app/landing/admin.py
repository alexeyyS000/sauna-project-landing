from django.contrib import admin

from . import models


@admin.register(models.PictureDecoration)
class PictureDecorationAdmin(admin.ModelAdmin):
    pass
