from django.db import models
import datetime
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
import django.utils.timezone


#monkey patching to make email field unique
User._meta.get_field('email')._unique = True



class Summary(models.Model):
    subjects = (
        ('english', 'english'),
        ('bible', 'bible'),
        ('history', 'history'),
        ('civics', 'civics'),
        ('language', 'language'),
        ('literature', 'literature'),
    )
    title = models.CharField(max_length=128)
    subject = models.CharField(max_length=20, choices=subjects)
    content = RichTextField(null=True, blank=True)
    date_created = models.DateTimeField(default=django.utils.timezone.now)
    date_edited = models.DateTimeField(blank=True, null=True)
    views = models.IntegerField(default=0)
    author = models.ForeignKey(User, default=1)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.title

    #custom save model
    def save(self, *args, **kwargs):
        #check if object is new
        if self.pk is not None:
            #get original content
            orig = Summary.objects.get(pk=self.pk)
            if orig.content != self.content:
                self.date_edited = datetime.datetime.now()
        else:
            self.date_created = datetime.datetime.now()

        super(Summary, self).save()

