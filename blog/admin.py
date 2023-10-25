from django.contrib import admin

from blog.models import Material


# Register your models here.


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', )
