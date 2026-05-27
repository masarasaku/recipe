from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse("Render deploy success!")

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('exe01/', include('helloapp.urls')),
    path('exe02/', include('bookapp.urls')),
    path('recipe/', include('recipeapp.urls')),
]
