from django.http import HttpResponse


# Create your views here.

def homePageView(request):
    return HttpResponse('Hello Web!')

def addView(request):
    first_num = int(request.GET.get('first'))
    sec_num = int(request.GET.get('second'))
    total = first_num + sec_num
    return HttpResponse('{}'.format(total))

def multView(request):
    first_num = int(request.GET.get('first'))
    sec_num = int(request.GET.get('second'))
    total = first_num * sec_num
    return HttpResponse('{}'.format(total))