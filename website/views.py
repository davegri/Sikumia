# -*- coding: UTF-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from website.models import Summary, View, Subject, Category, Subcategory, UserProfile
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.mail import send_mail
from website.forms import UserForm, CommentForm, SearchForm, SummaryForm, EditSummaryForm, CustomSignupForm, ChangePasswordForm, ChangeEmailForm, ContactForm
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
import datetime
import operator
from django.db.models import Q
from django.utils.translation import activate, override


import json

from functools import reduce
from django.core.cache import cache
from django.http import HttpResponseForbidden

def throttle(request, duration=15):
    """
        Goal of the function is to throttle requests from a user/bot
        returns true if user has been throttled
        returns false if user has not been throttled
    """
    if not request.user.is_staff:
        remote_addr = request.META.get('HTTP_X_FORWARDED_FOR') or \
                      request.META.get('REMOTE_ADDR')
        key = '%s.%s' % (remote_addr, request.get_full_path())
        if cache.get(key):
            expire_date = cache.get(key+'_expire_date')
            timedelta = expire_date - datetime.datetime.now()
            seconds_remaining = int(timedelta.total_seconds())
            messages.add_message(
            request, messages.ERROR,'אתה לא יכול לבצע פעולות כל כך מהר! חכה עוד {} שניות'.format(seconds_remaining))
            return True
        else:
            cache.set(key, 1, duration)
            cache.set(key+'_expire_date', datetime.datetime.now()+ datetime.timedelta(seconds = duration))

def index(request):
    context_dict = {}
    return render(request, 'index.html', context_dict)

def about(request):
    context_dict = {}
    return render(request, 'about.html', context_dict)

def contact(request):

    if request.method == "POST":
        form = ContactForm(data=request.POST)
        if form.is_valid():
            name = request.POST.get("name")
            user_subject = request.POST.get("subject")
            subject = "{} (from {})".format(user_subject,name)
            content = request.POST.get("content")
            from_email = request.POST.get("email")
            send_mail(subject, content, from_email, ["contact@sikumia.co.il"], fail_silently=False)
            messages.add_message(
                request,messages.SUCCESS,'הודעתך נשלחה בהצלחה')
            return redirect('contact')
    else:
        form = ContactForm()


    context_dict = {
        "form": form,
    }
    return render(request, 'contact.html', context_dict)

def sitemap(request):
    context_dict = {}
    return render(request, 'sitemap.html', context_dict)

def login(request):
    if request.POST:
        username = request.POST.get('login_username')
        password = request.POST.get('login_password')

        user = authenticate(username=username, password=password)
        if not user:
            messages.add_message(
                request, messages.ERROR, 'שם משתמש או סיסמא אינם נכונים', extra_tags='login')
        elif not user.is_active:
            messages.add_message(
                request, messages.ERROR, 'חשבונך נחסם, אם הינך חושב שזאת טעות צור קשר עם מנהל בהקדם.', extra_tags='login')
        else:
            django_login(request, user)
            return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))


def logout(request):
    django_logout(request)
    return redirect(request.META.get('HTTP_REFERER'))


def profile(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    summaries_list = user.summaries_authored.all()
    users_by_karma = sorted(UserProfile.objects.all(), key=lambda a: a.karma, reverse=True)
    rank = [i+1 for i,x in enumerate(users_by_karma) if x.pk == user.pk][0]
    # pagination
    paginator = Paginator(summaries_list, 12)

    # get page number from GET request
    page_num = request.GET.get('page', 1)

    # get summaries from paginator according to page number
    try:
        summaries = paginator.page(page_num)
    except(EmptyPage, InvalidPage):
        summaries = paginator.page(paginator.num_pages)

    context_dict = {
        'profile_user': user,
        'rank': rank,
        'summaries': summaries,
    }
    return render(request, 'profile.html', context_dict)


def settings(request, user_pk):
    if request.user.pk != int(user_pk):
        messages.add_message(
            request, messages.ERROR, 'אין לך הרשאות לבצע פעולה זו. אם הינך חושב שזאת טעות צור קשר עם הנהלת האתר')
        try:
            return redirect(request.META['HTTP_REFERER'])
        except KeyError:
            return redirect('index')

    if request.method == 'POST':
        if 'change_password' in request.POST:
            change_password_form = ChangePasswordForm(user=request.user, data=request.POST)
            if change_password_form.is_valid():
                user = get_object_or_404(User,pk=user_pk)
                user.set_password(change_password_form.cleaned_data.get('password'))
                user.save()
                messages.add_message(
                request, messages.SUCCESS, 'סיסמתך שונתה בהצלחה!')
                update_session_auth_hash(request,user)
                return redirect('settings',user_pk=user_pk)
            else:
                pass
        elif 'change_email' in request.POST:
            change_email_form = ChangeEmailForm(data=request.POST)
            if change_email_form.is_valid():
                user = get_object_or_404(User,pk=user_pk)
                user.email = change_email_form.cleaned_data.get('email')
                user.save()
                messages.add_message(
                request, messages.SUCCESS, 'כתובת אימייל עודכנה בהצלחה!')
                return redirect('settings',user_pk=user_pk)
    else:
        change_password_form = ChangePasswordForm(user=request.user)
        change_email_form = ChangeEmailForm(data={'email':request.user.email})

    context_dict = {
    'change_password_form': change_password_form,
    'change_email_form': change_email_form,
    }

    return render(request, 'settings.html', context_dict)


def subject(request, subject):
    summaries_list = Summary.objects.select_related().filter(
    subject__name=subject)
    subject = get_object_or_404(Subject.objects.prefetch_related('categories'), name=subject)
    category_list = subject.categories.prefetch_related('subcategory_set').all()
    length = len(summaries_list)
    categories_per_line = len(category_list)
    if subject.name == 'history_a':
        categories_per_line = 1
    # pagination
    paginator = Paginator(summaries_list, 10)

    # get page number from GET request
    page_num = request.GET.get('page', 1)

    # get summaries from paginator according to page number
    try:
        summaries = paginator.page(page_num)
    except(EmptyPage, InvalidPage):
        summaries = paginator.page(paginator.num_pages)

    context_dict = {
        'subject': subject,
        'categories': category_list,
        'sumAmount': length,
        'summaries': summaries,
        'categories_per_line': categories_per_line,
    }

    return render(request, 'subject.html', context_dict)


def category(request, subject, category):
    summaries_list = Summary.objects.all().filter(
        category__name__icontains=category)
    subject = get_object_or_404(Subject, name__icontains=subject)
    length = len(summaries_list)
    category = get_object_or_404(Category, name=category)
    subcategory_list = category.subcategory_set.all()
    # pagination
    paginator = Paginator(summaries_list, 12)

    # get page number from GET request
    page_num = request.GET.get('page', 1)

    # get summaries from paginator according to page number
    try:
        summaries = paginator.page(page_num)
    except(EmptyPage, InvalidPage):
        summaries = paginator.page(paginator.num_pages)

    context_dict = {
        'category': category,
        'subcategories': subcategory_list,
        'subject': subject,
        'sumAmount': length,
        'summaries': summaries,
    }

    return render(request, 'category.html', context_dict)


def subcategory(request, subject, category, subcategory):
    summaries_list = Summary.objects.all().filter(
        subcategory__name__icontains=subcategory)
    subject = get_object_or_404(Subject, name__icontains=subject)
    subcategory = get_object_or_404(Subcategory, name=subcategory, category__name=category)
    length = len(summaries_list)

    # pagination
    paginator = Paginator(summaries_list, 12)

    # get page number from GET request
    page_num = request.GET.get('page', 1)

    # get summaries from paginator according to page number
    try:
        summaries = paginator.page(page_num)
    except(EmptyPage, InvalidPage):
        summaries = paginator.page(paginator.num_pages)

    context_dict = {
        'subject': subject,
        'subcategory': subcategory,
        'sumAmount': length,
        'summaries': summaries,
    }

    return render(request, 'subcategory.html', context_dict)


# summary page

def summary(request, subject, category, subcategory, summary_id):
    try:
        summary = Summary.objects.get(pk=summary_id)
    except Summary.DoesNotExist:
        summary = "DOES NOT EXIST!"

    subject = Subject.objects.get(name=subject)

    request.session.save()
    if not View.objects.filter(summary=summary, session=request.session.session_key):
        view = View(summary=summary,
                    ip=request.META['REMOTE_ADDR'],
                    date_created=datetime.datetime.now(),
                    session=request.session.session_key)
        view.save()

    context_dict = {
        'subject': subject,
        'summary': summary,
    }

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        context_dict["comment_form"] = comment_form
        if comment_form.is_valid():
            if throttle(request):
                return render(request, "summary.html", context_dict)
            comment = comment_form.save(commit=False)
            comment.user = User.objects.get(id=request.user.id)
            comment.summary = summary
            comment.save()
            messages.add_message(request, messages.SUCCESS, 'התגובה שלך נוספה בצלחה')
            return redirect(comment)
        else:
            print(comment_form.errors)
    else:
        comment_form = CommentForm()
        context_dict["comment_form"] = comment_form

    return render(request, 'summary.html', context_dict)


def edit_summary(request, subject, category, subcategory, summary_id):
    instance = Summary.objects.get(pk=summary_id)
    if not request.user.pk == instance.author.pk:
        messages.add_message(
            request, messages.ERROR, 'אין לך הרשאות לבצע פעולה זו. אם הינך חושב שזאת טעות צור קשר עם הנהלת האתר')
        return redirect(instance)
    if request.method == "POST":
        summary_form = EditSummaryForm(request.POST, instance=instance)
        if summary_form.is_valid():
            summary_form.save()
            messages.add_message(
                request, messages.SUCCESS, 'הסיכום שלך נערך בהצלחה!')
            return redirect(instance)
        else:
            return HttpResponse(summary_form.errors)
    else:
        summary_form = EditSummaryForm(instance=instance)
    context_dict = {'summary_form': summary_form}
    return render(request, 'summary_edit.html', context_dict)


def rate_summary(request):
    summary_id = int(request.POST.get('id'))
    rate_type = request.POST.get('type')
    rate_action = request.POST.get('action')
    summary = get_object_or_404(Summary, pk=summary_id)
    ratings_to_return = -1
    if rate_action == 'rate':
        if rate_type == 'positive':
            summary.users_rated_positive.add(request.user)
            ratings_to_return = summary.users_rated_positive.count()
        elif rate_type == 'negative':
            summary.users_rated_negative.add(request.user)
            ratings_to_return = summary.users_rated_negative.count()
        else:
            return HttpResponse("RATING ERROR: rate_type must be either \"positive\" or \"negative\" ")
    elif rate_action == 'undo-rate':
        if rate_type == 'positive' and summary.users_rated_positive.filter(id=request.user.id).exists():
            summary.users_rated_positive.remove(request.user)
            ratings_to_return = summary.users_rated_positive.count()
        elif rate_type == 'negative' and summary.users_rated_negative.filter(id=request.user.id).exists():
            summary.users_rated_negative.remove(request.user)
            ratings_to_return = summary.users_rated_negative.count()
        else:
            return HttpResponse("RATING ERROR: unkown rating type OR user hasen't rated this summary")
    elif rate_action == 'change-type':
        # positive --> negative
        if rate_type == 'negative' and summary.users_rated_positive.filter(id=request.user.id).exists():
            summary.users_rated_positive.remove(request.user)
            summary.users_rated_negative.add(request.user)
            ratings_to_return = -2
        # negative --> positive
        elif rate_type == 'positive' and summary.users_rated_negative.filter(id=request.user.id).exists():
            summary.users_rated_negative.remove(request.user)
            summary.users_rated_positive.add(request.user)
            ratings_to_return = -2
        else:
            return HttpResponse("RATING ERROR: unkown rating type OR user hasen't rated this summary")        
    else:
        return HttpResponse("RATING ERROR: bad rate_action")

    return HttpResponse(ratings_to_return)

# register page


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            pass
    else:
        user_form = UserForm()

    return render(
        request,
        'register.html',
        {'user_form': user_form,
         'registered': registered})


def search(request):
    if request.method != "GET":
        return HttpResponse("request method needs to be GET")
    else:
        bound_search_form = SearchForm(request.GET)
        query = request.GET.get('query', False)
        subject = request.GET.get('subject')
        kwargs = {}
        args = []
        if query:
            query_word_list = query.split()
            args.append(reduce(operator.or_, ((
                Q(title__contains=x) | Q(content__contains=x)) for x in query_word_list)))

        if subject:
            kwargs['subject__name'] = subject

        summaries_list = Summary.objects.sortedByScore(*args, **kwargs)

        # get any current GET queries without the page modifier
        queries_without_page = request.GET.copy()
        if 'page' in queries_without_page.keys():
            del queries_without_page['page']

        length = len(summaries_list)

        # pagination
        paginator = Paginator(summaries_list, 10)

        # get page number from GET request
        page_num = request.GET.get('page', 1)

        # get summaries from paginator according to page number
        try:
            summaries = paginator.page(page_num)
        except(EmptyPage, InvalidPage):
            summaries = paginator.page(paginator.num_pages)

        context_dict = {
            'sumAmount': length,
            'summaries': summaries,
            'search_form': bound_search_form,
            'params': queries_without_page,
        }

        return render(request, 'search.html', context_dict)


def get_categories(request, subject_id):
    subject = Subject.objects.get(pk=subject_id)
    categories = subject.categories.all()
    html_string = ""
    for cat in categories:
        html_string += '<option value="%s">%s</option>' % (
            cat.pk, cat.hebrew_name)

    return HttpResponse(html_string, content_type="html")


def get_subcategories(request, category_id):
    category = Category.objects.get(pk=category_id)
    subcategories = category.subcategory_set.all()
    html_string = ""
    for subcat in subcategories:
        html_string += '<option value="%s">%s</option>' % (
            subcat.pk, subcat.hebrew_name)
    return HttpResponse(html_string, content_type="html")


def upload(request):
    if not request.user.is_authenticated():
        messages.add_message(
            request, messages.ERROR, 'עליך להיות מחובר כדי לבצע פעולה זו!')
        return redirect('/')
    if request.is_ajax():
        subject = list(request.POST.values())[0]
        categories = Subject.objects.get(
            pk=subject).category_set.all().values('hebrew_name', 'id')
        return HttpResponse(json.dumps(list(categories)))
    if request.method == "POST":
        summary_form = SummaryForm(request.POST)
        subject = request.POST["subject"]
        category = request.POST["category"]
        if request.POST["subject"]:
            summary_form.fields["category"].queryset = Category.objects.filter(subject=subject)
        if request.POST["category"]:
            summary_form.fields["subcategory"].queryset = Subcategory.objects.filter(category=category)
        if summary_form.is_valid():
            if throttle(request):
                return render(request, 'upload.html', {'summary_form': summary_form})
            summary = summary_form.save(commit=False)
            if summary_form.cleaned_data['new_user'] != "":
                if request.user.is_staff:
                    summary.author, created = User.objects.get_or_create(
                        username=summary_form.cleaned_data['new_user'],
                        defaults={'email':'%s@gmail.com' % summary_form.cleaned_data['new_user']})
                    if created:
                        summary.author.set_password('defaultpassword123')
                        summary.author.save()
            else:
                summary.author = User.objects.get(id=request.user.id)
            summary.save()
            messages.add_message(
                request, messages.SUCCESS, 'הסיכום שלך נוסף לאתר בהצלחה!')
            return redirect(summary)
        else:
            pass
    else:
        summary_form = SummaryForm()

    context_dict = {'summary_form': summary_form}

    return render(request, 'upload.html', context_dict)


def leaderboard(request):
    user_list = sorted(User.objects.all(), key=lambda a: a.profile.karma, reverse=True)[:10]
    context_dict = {'user_list': user_list}
    return render(request, 'leaderboard.html', context_dict)    