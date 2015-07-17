# -*- coding: UTF-8 -*-
from django.contrib.auth.models import User
from django import forms
from .models import Comment, Summary
from ckeditor.fields import RichTextField


class UserForm(forms.ModelForm):
    required_message = "שזה זה הינו חובה"
    username_unique_message = "שם המשתמש שבחרת כבר קיים במערכת, בחר שם אחר"
    email_unique_message = "כתובת האמייל שבחרת כבר קיימת במערכת"
    password = forms.CharField(
        widget=forms.PasswordInput(), error_messages={'required': required_message},)
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(), error_messages={'required': required_message},)
    username = forms.CharField(
        error_messages={'unique': username_unique_message, 'required': required_message})
    email = forms.CharField(
        error_messages={'unique': email_unique_message, 'required': required_message})

    def clean_confirm_password(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('confirm_password')
        if password1 != password2:
            raise forms.ValidationError("הסיסמאות שהכנסת אינן תואמות")
        return password2

    def is_valid(self):
        ret = forms.Form.is_valid(self)
        for f in self.errors:
            self.fields[f].widget.attrs.update({'class': 'invalid'})
        return ret

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('content',)

class SummaryForm(forms.ModelForm):
    class Meta:
        model = Summary
        fields = ('title', 'subject', 'content', 'subject_division')

    def __init__(self, *args, **kwargs):
        super(SummaryForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = "הכנס כותרת לסיכום"
        self.fields['subject'].label = "בחר מקצוע"
        self.fields['content'].label = "תוכן הסיכום"


class EditSummaryForm(forms.ModelForm):
    class Meta:
        model = Summary
        fields = ('title','content')

class SearchForm(forms.Form):

    subjects = (
        ('all', "כל המקצועות"),
        ('english', 'אנגלית'),
        ('bible', 'תנ"ך'),
        ('history', 'היסטוריה'),
        ('civics', 'אזרחות'),
        ('language', 'לשון'),
        ('literature', 'ספרות'),
    )
    orders = (
        ("popularity", 'פופולריות'),
        ("date_added", 'נוסף לאחרונה'),
        ("date_edited", 'נערך לאחורנה'),
    )

    query = forms.CharField(max_length=100)
    subject = forms.ChoiceField(choices=subjects)
    order_by = forms.ChoiceField(choices=orders)

