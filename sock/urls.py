from django.urls import path, include
from rest_framework.routers import DefaultRouter

# from .views import SockList

# router = DefaultRouter()
# router.register(r"sock", SockList)

# urlpatterns = [
#     path("", include(router.urls))
# ]

from sock import views

urlpatterns = [
    path("sock/", views.sock_list),
    path("sock/<int:pk>", views.sock_detail),

]