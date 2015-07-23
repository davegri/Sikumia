# -*- coding: UTF-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from website.models import Summary, View, Subject, Category, Subcategory
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from website.forms import UserForm, CommentForm, SearchForm, SummaryForm, EditSummaryForm
from django.template import RequestContext
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import resolve
from django.contrib import messages
import datetime
import operator
from django.db.models import Q
from django.utils.translation import activate

from django.core import serializers
import json

from functools import reduce


from django.utils.http import urlencode


def get_query_string(params, new_params=None, remove=None):
    if new_params is None:
        new_params = {}
    if remove is None:
        remove = []
    p = params.copy()
    for r in remove:
        for k in p.keys():
            if k.startswith(r):
                del p[k]
                break
    for k, v in new_params.items():
        if v is None:
            if k in p:
                del p[k]
        else:
            p[k] = v
    return '?%s' % urlencode(p)


def index(request):
    context_dict = {}
    return render(request, 'index.html', context_dict)


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
    user = get_object_or_404(User,pk=user_pk)
    summaries_list = user.summaries_authored.all()
    positive_karma = sum([summary.users_rated_positive.count() for summary in summaries_list])
    negative_karma = sum([summary.users_rated_negative.count() for summary in summaries_list])
    karma = positive_karma - negative_karma

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
            'profile_user':user,
            'karma':karma,
            'summaries': summaries,
    }
    return render(request, 'profile.html', context_dict)


def subject(request, subject):
    summaries_list = Summary.objects.all().filter(
        subject__name__icontains=subject)
    subject = get_object_or_404(Subject, name__icontains=subject)
    category_list = subject.category_set.filter()
    length = len(summaries_list)
    categories_per_line = len(category_list)
    if subject.name == 'history_a':
        categories_per_line = 1
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
    category = get_object_or_404(Category,name=category)
    subcategory_list = category.subcategory_set.all()
    subcategories_per_line = len(subcategory_list)
    if subject.name == 'history_a':
        subcategories_per_line = 1
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
        'category':category,
        'subcategories': subcategory_list,
        'subject': subject,
        'sumAmount': length,
        'summaries': summaries,
        'subcategories_per_line': subcategories_per_line,
    }

    return render(request, 'category.html', context_dict)

def subcategory(request, subject, category, subcategory):
    summaries_list = Summary.objects.all().filter(
        subcategory__name__icontains=subcategory)
    subject = get_object_or_404(Subject, name__icontains=subject)
    subcategory = get_object_or_404(Subcategory, name=subcategory)
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


def summary(request, subject, category, summary_id):
    try:
        summary = Summary.objects.get(pk=summary_id)
    except Summary.DoesNotExist:
        summary = "DOES NOT EXIST!"

    request.session.save()
    if not View.objects.filter(summary=summary, session=request.session.session_key):
        view = View(summary=summary,
                           ip=request.META['REMOTE_ADDR'],
                           date_created=datetime.datetime.now(),
                           session=request.session.session_key)
        view.save()

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = User.objects.get(id=request.user.id)
            comment.summary = summary
            comment.save()
        else:
            print(comment_form.errors)
    else:
        comment_form = CommentForm()

    context_dict = {
        'subject': subject,
        'summary': summary,
        'comment_form': comment_form
    }
    return render(request, 'summary.html', context_dict)


def edit_summary(request, subject, category, summary_id):
    instance = Summary.objects.get(pk=summary_id)
    if not request.user.pk == instance.author.pk:
        messages.add_message(request, messages.ERROR, 'אין לך הרשאות לבצע פעולה זו. אם הינך חושב שזאת טעות צור קשר עם הנהלת האתר')
        return redirect(instance)
    activate('he')
    if request.method == "POST":
        summary_form = EditSummaryForm(request.POST, instance=instance)
        if summary_form.is_valid():
            summary_form.save()
            messages.add_message(request, messages.SUCCESS, 'הסיכום שלך נערך בהצלחה!')
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
    thisUserPositiveRatings = summary.users_rated_positive.filter(
        id=request.user.id).count()
    thisUserNegativeRatings = summary.users_rated_negative.filter(
        id=request.user.id).count()
    ratings_to_return = -1
    if rate_action == 'rate':
        if thisUserPositiveRatings == 0 and thisUserNegativeRatings == 0:
            if rate_type == 'positive':
                summary.users_rated_positive.add(request.user)
                ratings_to_return = summary.users_rated_positive.count()
            elif rate_type == 'negative':
                summary.users_rated_negative.add(request.user)
                ratings_to_return = summary.users_rated_negative.count()
            else:
                return HttpResponse("RATING ERROR: rate_type must be either \"positive\" or \"negative\" ")
        else:
            return HttpResponse("RATING ERROR: %s has already rated this summary " % request.user.username)
    elif rate_action == 'undo-rate':
        if rate_type == 'positive' and thisUserPositiveRatings == 1:
            summary.users_rated_positive.remove(request.user)
            ratings_to_return = summary.users_rated_positive.count()
        elif rate_type == 'negative' and thisUserNegativeRatings == 1:
            summary.users_rated_negative.remove(request.user)
            ratings_to_return = summary.users_rated_negative.count()
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
        query = request.GET['query']
        kwargs = {}
        args = []
        if query:
            query_word_list = query.split()
            args.append(reduce(operator.or_, ((
                Q(title__contains=x) | Q(content__contains=x)) for x in query_word_list)))

        summaries_list = Summary.objects.sortedByScore(*args, **kwargs)

        # get any current GET queries without the page modifier
        queries_without_page = request.GET.copy()
        if 'page' in queries_without_page.keys():
            del queries_without_page['page']

        length = len(summaries_list)

        # pagination
        paginator = Paginator(summaries_list, 15)

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
            'queries': queries_without_page,
        }

        return render(request, 'search.html', context_dict)

def get_categories(request, subject_id):
    subject = Subject.objects.get(pk=subject_id)
    categories = subject.category_set.all()
    html_string=""
    for cat in categories:
        html_string += '<option value="%s">%s</option>' % (cat.pk, cat.hebrew_name)

    return HttpResponse(html_string, content_type="html")
def get_subcategories(request, category_id):
    category = Category.objects.get(pk=category_id)
    subcategories = category.subcategory_set.all()
    html_string=""
    for subcat in subcategories:
        html_string += '<option value="%s">%s</option>' % (subcat.pk, subcat.hebrew_name)
    return HttpResponse(html_string, content_type="html")


def upload(request):

    if not request.user.is_authenticated():
        messages.add_message(request, messages.ERROR, 'עליך להיות מחובר כדי לבצע פעולה זו!')
        return redirect('/')
    if request.is_ajax():
        subject = list(request.POST.values())[0]

        categories = Subject.objects.get(pk=subject).category_set.all().values('hebrew_name','id')
        return HttpResponse(json.dumps(list(categories)))
    activate('he')
    if request.method == "POST":
        summary_form = SummaryForm(request.POST)
        if summary_form.is_valid():
            summary = summary_form.save(commit=False)
            summary.author = User.objects.get(id=request.user.id)
            summary.save()
            messages.add_message(request, messages.SUCCESS, 'הסיכום שלך נוסף לאתר בהצלחה!')
            return redirect(summary)
        else:
            pass
    else:
        summary_form = SummaryForm()

    context_dict = {'summary_form': summary_form}

    return render(request, 'upload.html', context_dict)
