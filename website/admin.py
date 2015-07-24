from django.contrib import admin
from website import models
from django.contrib.auth.models import User
from adminsortable.admin import SortableAdmin, SortableStackedInline, SortableTabularInline
# Register your models here.


class CommentInline(admin.TabularInline):
	model = models.Comment
	extra = 0
admin
class SummaryInline(admin.TabularInline):
      model = models.Summary
      extra = 1

class CateogryInline(SortableTabularInline):
    model = models.Category
    extra = 1
    
class SubcateogryInline(SortableTabularInline):
    model = models.Subcategory
    extra = 1

class SummaryAdmin(admin.ModelAdmin):
    list_filter = ['date_created','date_edited','subject',]
    search_fields = ['title','content']
    list_display = ['title','subject', 'date_created','date_edited','_comments','_score']
    inlines = [CommentInline]

    def _comments(self, obj):
        return obj.comments.all().count()
    def _score(self, obj):
    	return obj.get_score()

class CommentAdmin(admin.ModelAdmin):
	list_display = ['summary','user','content','date_created']

class UserAdmin(admin.ModelAdmin):
    inlines = [SummaryInline,CommentInline]

class SubjectAdmin(SortableAdmin):
    inlines = [CateogryInline]

class CategoryAdmin(SortableAdmin):
    inlines = [SubcateogryInline]






admin.site.register(models.Summary,SummaryAdmin)
admin.site.register(models.Comment,CommentAdmin)
admin.site.register(models.Subject,SubjectAdmin)
admin.site.register(models.Category,CategoryAdmin)

admin.site.unregister(User)
admin.site.register(User,UserAdmin)