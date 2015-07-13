from django.contrib import admin
from website import models
# Register your models here.


class SummaryAdmin(admin.ModelAdmin):
    list_filter = ['date_created','date_edited','subject']
    search_fields = ['title','content']
    list_display = ['title','subject', 'date_created','date_edited']

class CommentAdmin(admin.ModelAdmin):
	list_display = ['summary','user','content','date_created']

admin.site.register(models.Summary,SummaryAdmin)
admin.site.register(models.Comment,CommentAdmin)