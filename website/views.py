# -*- coding: UTF-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from website.models import Summary
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from website.forms import UserForm
from django.template import RequestContext
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.core.urlresolvers import resolve
from django.contrib import messages


def index(request):
    context_dict = {}
    return render(request, 'index.html', context_dict)



def login(request):
    if request.POST:
        username = request.POST.get('login_username')
        password = request.POST.get('login_password')

        user = authenticate(username=username, password=password)

        if not user:
            messages.add_message(request, messages.INFO, 'שם משתמש או סיסמא אינם נכונים') 
        elif not user.is_active:
            messages.add_message(request, messages.INFO, 'חשבונך נחסם, אם הינך חושב שזאת טעות צור קשר עם מנהל בהקדם.') 
        else:
            django_login(request,user)
            return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))


def logout(request):
    django_logout(request)
    return redirect(request.META.get('HTTP_REFERER'))



#subject page


def subject(request, subject):

    hebSubjects = {
        'english': 'אנגלית',
        'bible': 'תנ"ך',
        'history': 'היסטוריה',
        'civics': 'אזרחות',
        'language': 'לשון',
        'literature': 'ספרות',
    }

    if subject not in hebSubjects:
        return redirect('/sikumim')

    summaries_list = Summary.objects.all().filter(subject=subject)
    length = len(summaries_list)

    #pagination
    paginator = Paginator(summaries_list, 4)

    #get page number from GET request
    page_num = request.GET.get('page', 1)

    #get summaries from paginator according to page number
    try:
        summaries = paginator.page(page_num)
    except(EmptyPage, InvalidPage):
        summaries = paginator.page(paginator.num_pages)

    context_dict = {
        'subject': subject,
        'hebSubject': hebSubjects[subject],
        'sumAmount': length,
        'summaries': summaries,
    }

    return render(request, 'subject.html', context_dict)

#summary page


def summary(request, subject, pk):
    try:
        summary = Summary.objects.get(pk=pk)
    except Summary.DoesNotExist:
        summary = "DOES NOT EXIST!"

    context_dict = {
        'subject': subject,
        'summary': summary,
        }

    return render(request, 'summary.html', context_dict)


def rate_summary(request):
    summary_id = int(request.POST.get('id'))
    rate_type = request.POST.get('type')
    rate_action = request.POST.get('action')
    summary = get_object_or_404(Summary, pk=summary_id)
    thisUserPositiveRatings = summary.positive_ratings.filter(id=request.user.id).count()
    thisUserNegativeRatings = summary.negative_ratings.filter(id=request.user.id).count()
    ratings_to_return = -1
    if rate_action == 'rate':
        if thisUserPositiveRatings == 0 and thisUserNegativeRatings == 0:
            if rate_type == 'positive':
                summary.positive_ratings.add(request.user)
                ratings_to_return = summary.positive_ratings.count()
            elif rate_type == 'negative':
                summary.negative_ratings.add(request.user)
                ratings_to_return = summary.negative_ratings.count()
            else:
                return HttpResponse("RATING ERROR: rate_type must be either \"positive\" or \"negative\" ")
        else:
            return HttpResponse("RATING ERROR: %s has already rated this summary " %request.user.username)
    elif rate_action == 'undo-rate':
        if rate_type == 'positive' and thisUserPositiveRatings == 1:
            summary.positive_ratings.remove(request.user)
            ratings_to_return = summary.positive_ratings.count()
        elif rate_type == 'negative' and thisUserNegativeRatings == 1:
            summary.negative_ratings.remove(request.user)
            ratings_to_return = summary.negative_ratings.count()
        else:
            return HttpResponse("RATING ERROR: unkown rating type OR user hasen't rated this summary")
    else:
        return HttpResponse("RATING ERROR: bad rate_action")


    return HttpResponse(ratings_to_return)

#register page
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
            print (user_form.errors)
    else:
        user_form = UserForm()

    return render(
        request,
        'register.html',
        {'user_form': user_form,
         'registered': registered})
