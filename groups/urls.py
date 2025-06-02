from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('groups/', views.groups_list, name='groups_list'),
    path('groups/create/', views.create_group, name='create_group'),
    path('groups/<int:pk>/', views.group_detail, name='group_detail'),
    path('groups/<int:pk>/join/', views.join_group, name='join_group'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('profile/', views.profile_view, name='profile'),
    path('register/', views.register_view, name='register'),
]
