from django.http import HttpResponse

# Create your views here.

def show_hello(request):
    return HttpResponse("ハロー, Django!")