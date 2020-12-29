from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Account
from django.db.models import Q
import json



@login_required
def addView(request):
	user = User.objects.get(username = request.user)
	print(user)
	print(request.POST.get("iban"))
	account = Account.objects.create(owner=user, iban=request.POST.get("iban"))
	print(Account.objects.filter(owner=user))
	return redirect('/')


@login_required
def homePageView(request):
	try:
		list = Account.objects.filter(owner__username=request.user)
	except Account.DoesNotExist:
		print('here')
		list = []
	
	accounts = []
	for item in list:
		accounts.append(item)

	for a in accounts:
		print(type(a.iban))


	return render(request, 'pages/index.html', {"accounts": accounts})
