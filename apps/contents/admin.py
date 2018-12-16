from django.contrib import admin
from apps.contents import models
# Register your models here.
admin.site.register(models.ContentCategory)
admin.site.register(models.Content)