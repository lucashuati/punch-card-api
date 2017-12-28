from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from punch_card import views

urlpatterns = [
    path('', views.PunchCardList.as_view(), name='index'),
    path('<int:pk>/', views.PunchCardDetail.as_view(), name='detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
