'''
I added these url configs.
'''
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from sock import views
from .views import SockList

urlpatterns = [
    path("sock/", views.SockList.as_view()),
    path("sock/<int:id>", views.sock_detail), # was struggling with errors from routes without slash, added this route just to be safe
    path("sock/<int:id>/", views.sock_detail),
    path("pairs/", views.pair_list),

]