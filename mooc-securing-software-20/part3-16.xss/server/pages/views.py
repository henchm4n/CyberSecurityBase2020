from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Message, Mail
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import json


# This view simulates an external mail server receiving a stolen cookie
@csrf_exempt 
def mailView(request):
	Mail.objects.create(content=request.body.decode('utf-8'))
	print(request.body.decode('utf-8'))
	return HttpResponse('')
	

@login_required
def addView(request):
	target = User.objects.get(username=request.POST.get('to'))
	Message.objects.create(source=request.user, target=target, content=request.POST.get('content'))
	return redirect('/')


@login_required
def homePageView(request):
	messages = Message.objects.filter(Q(source=request.user) | Q(target=request.user))
	users = User.objects.exclude(pk=request.user.id)
	return render(request, 'pages/index.html', {'msgs': messages, 'users': users})
