from django.urls import path
from app.settings import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contacts/', views.contacts, name='contacts'),
    path('menu/', views.menu, name='menu'),
    path('gallery/', views.gallery, name='gallery'),
    path('reservation/', views.reservation, name='reservation'),
    path('reviews/', views.reviews, name='reviews'),
    path('news/', views.news_list, name='news_list'),
]