from django.urls import path, include
from rest_framework.routers import DefaultRouter
from sock import views
from .views import SockList

urlpatterns = [
    path("sock/", views.SockList.as_view()),
    path("sock/<int:id>", views.sock_detail),
    path("sock/<int:id>/", views.sock_detail),
    path("pairs/", views.pair_list),

]