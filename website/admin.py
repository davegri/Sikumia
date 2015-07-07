from django.contrib import admin
from website import models
# Register your models here.


class SummaryAdmin(admin.ModelAdmin):
    list_filter = ['date_created','date_edited','subject','views']
    search_fields = ['title','content']
    list_display = ['title','subject','views','date_created','date_edited']

admin.site.register(models.Summary,SummaryAdmin)