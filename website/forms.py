# -*- coding: UTF-8 -*-
from django.contrib.auth.models import User
from django import forms
from .models import Comment, Summary, Category, Subcategory, Subject
from ckeditor.fields import RichTextField

from allauth.socialaccount.forms import SignupForm

from django.utils.translation import activate

from django.contrib.auth.forms import PasswordResetForm

from captcha.fields import ReCaptchaField


class UserForm(forms.ModelForm):
    captcha = ReCaptchaField()
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

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['captcha'].error_messages = {'required': 'עלייך לסמן שאתה לא רובוט'}


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('content',)

class ChangePasswordForm(forms.ModelForm):

    old_password = forms.CharField(widget=forms.PasswordInput())
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('password',)

    def __init__(self, user, data=None):
        self.user = user
        super(ChangePasswordForm, self).__init__(data=data)

    def clean_old_password(self):
        password = self.cleaned_data.get('old_password')
        if not self.user.check_password(password):
            raise forms.ValidationError('סיסמא נוכחית שגויה, נסה שוב')
        return password

    def clean_confirm_password(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('confirm_password')

        if password1 != password2:
            raise forms.ValidationError('הסיסמאות שהכנסת איתן תואמות')
        return password2

    def is_valid(self):
        ret = forms.Form.is_valid(self)
        for f in self.errors:
            self.fields[f].widget.attrs.update({'class': 'invalid'})
        return ret

class ChangeEmailForm(forms.Form):
    email = forms.EmailField()

class SummaryForm(forms.ModelForm):
    new_user = forms.CharField(max_length=30, required=False, label="add as a new user")
    category = forms.ModelChoiceField(queryset=Category.objects.none(), empty_label="בחר מקצוע כדי לבחור נושא")
    subcategory = forms.ModelChoiceField(queryset=Subcategory.objects.none(), empty_label="בחר נושא כדי לבחור תת נושא")
    class Meta:
        model = Summary
        fields = ('title','subject', 'content', 'category', 'subcategory')
    def is_valid(self):
        ret = forms.Form.is_valid(self)
        for f in self.errors:
            self.fields[f].widget.attrs.update({'class': 'invalid'})
        return ret

    def __init__(self, *args, **kwargs):
        super(SummaryForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = "הכנס כותרת לסיכום"
        self.fields['title'].error_messages = {'required': 'עליך לבחור כותרת לסיכום!'}
        self.fields['subject'].label = "בחר מקצוע"
        self.fields['subject'].error_messages = {'required': 'בחר מקצוע!'}
        self.fields['content'].label = "תוכן הסיכום"
        self.fields['category'].label = "בחר נושא"
        self.fields['category'].error_messages = {'required': 'עליך לבחור נושא רלוונטי!'}
        self.fields['subcategory'].label = "בחר תת נושא"
        self.fields['subcategory'].error_messages = {'required': 'עליך לבחור תת נושא רלוונטי!'}



class EditSummaryForm(forms.ModelForm):
    class Meta:
        model = Summary
        fields = ('title','content')

class SearchForm(forms.Form):
    subject_queryset = Subject.objects.all()
    query = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'הקלד מילות חיפוש, לדוגמא - "הזכות להליך הוגן"'}))
    subject = forms.ModelChoiceField(queryset=subject_queryset, empty_label='הכל', to_field_name='name')


class CustomSignupForm(SignupForm):

    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)

    def raise_duplicate_email_error(self):
        raise forms.ValidationError("שם משתמש כבר קיים עם כתובת אימייל זאת, נסה להתחבר בראש האתר.")



class CustomPasswordResetForm(PasswordResetForm):
    def is_valid(self):
        ret = forms.Form.is_valid(self)
        for f in self.errors:
            self.fields[f].widget.attrs.update({'class': 'invalid'})
        return ret
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('כתובת אימייל זאת לא קיימת במערכת!')
        return email