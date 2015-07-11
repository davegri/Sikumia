# -*- coding: UTF-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from website.models import Summary
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from website.forms import UserForm
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout



def index(request):
    #login/logout logic
    if request.method == 'POST':
        if 'logout' not in request.POST:
            username = request.POST.get('login_username')
            password = request.POST.get('login_password')
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request,user)
                    return redirect(request.META.get('HTTP_REFERER'))
                else:
                    return HttpResponse("Your account is disabled.")
            else:
                return HttpResponse("invalid login details")
        else:
            logout(request)
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        context_dict = {}
        return render(request, 'index.html', context_dict)


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
