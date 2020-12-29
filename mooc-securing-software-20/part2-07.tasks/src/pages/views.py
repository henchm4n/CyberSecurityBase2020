from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

tasks = ['Wash the car', 'Finish the project', 'Build a time machine']

@csrf_exempt
def taskView(request):
	return JsonResponse({'tasks' : [{'name': t} for t in tasks]})


@csrf_exempt # this exempt would not be ok in production without replacement csrf protection
def addView(request):
	name = 'untitled'
	if request.method == 'POST':
		body = json.loads(request.body)
		name = body.get('name', 'untitled').strip()

	tasks.append(name)
	return JsonResponse({'name' : name})


def homePageView(request):
	# shorter way of writing instead of loader
	return render(request, 'pages/tasks.html')
