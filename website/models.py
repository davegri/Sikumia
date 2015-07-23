from django.db import models
import datetime
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
import django.utils.timezone
from adminsortable.models import Sortable, SortableForeignKey
from math import sqrt
import bleach

# monkey patching to make email field unique
User._meta.get_field('email')._unique = True


class Subject(Sortable):
    name = models.CharField(max_length=100)
    hebrew_name = models.CharField(max_length=100)
    color = models.CharField(max_length=6)

    class Meta(Sortable.Meta):
        pass

    def __str__(self):
        return self.hebrew_name

    def get_absolute_url(self):
        return "/subject/%s/" % (self.name)


class Category(Sortable):
    name = models.CharField(max_length=100)
    hebrew_name = models.CharField(max_length=100)
    subject = SortableForeignKey(Subject)

    class Meta(Sortable.Meta):
        pass

    def __str__(self):
        return self.hebrew_name

    def get_absolute_url(self):
        return "/subject/%s/%s" % (self.subject.name, self.name)


class Subcategory(Sortable):
    name = models.CharField(max_length=100)
    hebrew_name = models.CharField(max_length=100)
    category = SortableForeignKey(Category)

    class Meta(Sortable.Meta):
        pass

    def __str__(self):
        return self.hebrew_name

    def get_absolute_url(self):
        return "/subject/%s/%s/%s" % (self.category.subject.name, self.category.name, self.name)


class SummaryManager(models.Manager):

    def sortedByScore(self, *args, **kwargs):
        summaries = self.get_queryset().filter(*args, **kwargs)
        return sorted(summaries, key=lambda summary: summary.get_score(), reverse=True)


class Summary(models.Model):
    title = models.CharField(max_length=128)
    subject = models.ForeignKey(Subject)
    category = models.ForeignKey(Category)
    subcategory = models.ForeignKey(Subcategory)
    content = RichTextField(null=True, blank=True)
    users_rated_positive = models.ManyToManyField(
        User, blank=True, related_name='summaries_rated_positive')
    users_rated_negative = models.ManyToManyField(
        User, blank=True, related_name='summaries_rated_negative')
    author = models.ForeignKey(User, related_name='summaries_authored')
    users_bookmarked = models.ManyToManyField(
        User, related_name='summaries_bookmarked', blank=True)
    date_created = models.DateTimeField(default=django.utils.timezone.now)
    date_edited = models.DateTimeField(blank=True, null=True)

    objects = SummaryManager()

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/subject/%s/%s/%i/" % (self.subject.name, self.category.name, self.id)

    def get_score(self):
        ups = self.users_rated_positive.count()
        downs = self.users_rated_negative.count()
        if ups == 0:
            return -downs
        n = ups + downs
        z = 1.64485  # 1.0 = 85%, 1.6 = 95%
        phat = float(ups) / n
        return (phat + z * z / (2 * n) - z * sqrt((phat * (1 - phat) + z * z / (4 * n)) / n)) / (1 + z * z / n)

    # custom save model
    def save(self, *args, **kwargs):
        # clean raw html to prevent xss attack
        ALLOWED_ATTRIBUTES = {
            '*': ['style']
        }
        ALLOWED_TAGS = ['h1','h2','h3','h4','h5','h6','p', 'em', 'strong', 'blockquote', 'code', 'strike'
         'br', 'td', 'tr', 'small', 'hr', 'table','tbody', 'b', 'u', 'ul', 'ol', 'li', 'img', 'pre'
         'strong', 'sub', 'i', 'del', 'dd', 'dl', 'sup']
        ALLOWED_STYLES = ['color', 'font-weight', 'font-size']
        self.content = bleach.clean(self.content,tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES,
          styles=ALLOWED_STYLES,strip=True)
        # check if object is new
        if self.pk is not None:
                # get original content
            orig = Summary.objects.get(pk=self.pk)
            if orig.content != self.content:
                self.date_edited = datetime.datetime.now()
        else:
            self.date_created = datetime.datetime.now()

        super(Summary, self).save()


class View(models.Model):
    summary = models.ForeignKey(Summary, related_name='views')
    ip = models.CharField(max_length=40)
    session = models.CharField(max_length=40)
    date_created = models.DateTimeField(default=django.utils.timezone.now)


class Comment(models.Model):
    summary = models.ForeignKey(Summary, related_name='comments')
    user = models.ForeignKey(User, related_name='comments')
    content = models.TextField(max_length=1000)
    date_created = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return self.summary.get_absolute_url() + "#%i" % self.id
