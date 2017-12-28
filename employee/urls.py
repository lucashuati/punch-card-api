from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from employee import views

urlpatterns = [
    path('', views.EmployeeList.as_view(), name='index'),
    path('<int:pk>/', views.EmployeeDetail.as_view(), name='detail'),
    path('<int:pk>/acumulate/', views.GetAcumulate.as_view(), name='acumulate'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
