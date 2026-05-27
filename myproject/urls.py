from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('exe01/', include('helloapp.urls')),
    path('exe02/', include('bookapp.urls')),
    path('recipe/', include('recipeapp.urls')),
]
