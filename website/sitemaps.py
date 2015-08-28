from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse
from .models import Comment, Summary, Category, Subcategory, Subject

class SummarySitemap(Sitemap):
    changefreq = "hourly"

    def items(self):
        return Summary.objects.all()

class SubjectSitemap(Sitemap):
    changefreq = "yearly"

    def items(self):
        return Subject.objects.all()

class CategorySitemap(Sitemap):
    changefreq = "yearly"

    def items(self):
        return Category.objects.all()

class SubcategorySitemap(Sitemap):
    changefreq = "yearly"

    def items(self):
        return Subcategory.objects.all()


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['register', 'search', 'about', 'leaderboard']

    def location(self, item):
        return reverse(item)
        
