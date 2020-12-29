from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Account


def balanceView(request):
	if request.user.is_authenticated:
		return JsonResponse({'username': request.user.username, 'balance': request.user.account.balance})
	else:
		return JsonResponse({'username': 'anonymous', 'balance': 0})
	


@login_required
def homePageView(request):
	accounts = Account.objects.exclude(user_id=request.user.id)
	return render(request, 'pages/index.html', {'accounts': accounts})
