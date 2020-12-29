from django.http import HttpResponse
from .models import Message


# Create your views here.

def homePageView(request):
	content = 'Hello Web!'
	value = request.GET['id']

	object = Message.objects.get(id=value)
		
	return HttpResponse(object.content)
