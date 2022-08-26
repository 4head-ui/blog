from django.urls import path
from . import views
#"""Определяет схемы URL для learning_logs."""

app_name = 'main'
urlpatterns=[
    path('', views.index, name='index'),
    path('learn', views.learn, name='learn'),
    path('topics/', views.topics, name='topics'),
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    path('new_topic/', views.new_topic, name='new_topic'),
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),

]