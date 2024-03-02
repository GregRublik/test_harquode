from django.contrib import admin
from django.urls import path

from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('max_values/', views.distribute_max_values),
    path('refresh_groups/', views.refresh_list_groups),
]
