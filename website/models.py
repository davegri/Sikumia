from django.db import models
import datetime
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
import django.utils.timezone
from math import sqrt

# monkey patching to make email field unique
User._meta.get_field('email')._unique = True


class SummaryManager(models.Manager):
    def sortedByScore(self, *args, **kwargs):
        summaries = self.get_queryset().filter(*args, **kwargs)
        return sorted(summaries, key=lambda summary: summary.get_score(),reverse=True)


class Summary(models.Model):
    subjects = (
        ('english', 'english'),
        ('bible', 'bible'),
        ('history', 'history'),
        ('civics', 'civics'),
        ('language', 'language'),
        ('literature', 'literature'),
    )
    grades = (
        (10, 'Grade 10'),
        (11, 'Grade 11'),
        (12, 'Grade 12'),
    )

    title = models.CharField(max_length=128)
    grade = models.IntegerField(choices=grades)
    subject = models.CharField(max_length=20, choices=subjects)
    content = RichTextField(null=True, blank=True)
    positive_ratings = models.ManyToManyField(
        User, blank=True, related_name='summaries_rated_positive')
    negative_ratings = models.ManyToManyField(
        User, blank=True, related_name='summaries_rated_negative')
    author = models.ForeignKey(User, related_name='summaries_authored')
    bookmarks = models.ManyToManyField(
        User, related_name='summaries_bookmarked', null=True, blank=True)
    date_created = models.DateTimeField(default=django.utils.timezone.now)
    date_edited = models.DateTimeField(blank=True, null=True)

    def get_score(self):
        ups = self.positive_ratings.count()
        downs = self.negative_ratings.count()
        if ups == 0:
            return -downs
        n = ups + downs
        z = 1.64485  # 1.0 = 85%, 1.6 = 95%
        phat = float(ups) / n
        return (phat + z * z / (2 * n) - z * sqrt((phat * (1 - phat) + z * z / (4 * n)) / n)) / (1 + z * z / n)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.title

    # custom save model
    def save(self, *args, **kwargs):
        # check if object is new
        if self.pk is not None:
            # get original content
            orig = Summary.objects.get(pk=self.pk)
            if orig.content != self.content:
                self.date_edited = datetime.datetime.now()
        else:
            self.date_created = datetime.datetime.now()

        super(Summary, self).save()

    objects = SummaryManager()


class SummaryView(models.Model):
    summary = models.ForeignKey(Summary, related_name='views')
    ip = models.CharField(max_length=40)
    session = models.CharField(max_length=40)
    date_created = models.DateTimeField(default=django.utils.timezone.now)

class Comment(models.Model):
    summary = models.ForeignKey(Summary, related_name='comments')
    user = models.ForeignKey(User, related_name='comments')
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)

