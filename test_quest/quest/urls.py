from django.contrib import admin
from django.urls import path
from main import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('max_values/', views.distribute_max_values),
    path('refresh_groups/', views.refresh_list_groups),
    path('products/', views.ProductViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('products/<int:pk>/', views.ProductViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('lessons/', views.LessonViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('lessons/<int:pk>/', views.LessonViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
]
