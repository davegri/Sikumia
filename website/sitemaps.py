from django.contrib.sitemaps import Sitemap
from .models import Comment, Summary, Category, Subcategory, Subject

class SummarySitemap(Sitemap):
    changefreq = "weekly"

    def items(self):
        return Summary.objects.all()

        
