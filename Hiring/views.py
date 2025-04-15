from django.http import HttpResponse

def home(request):
    return HttpResponse("This is the Home page for hiring")


def about(request):
    return HttpResponse("This is the About page for hiring")


def contact(request):
    return HttpResponse("You can contact the admin of the website")