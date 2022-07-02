from django.urls import path, include
from rest_framework.routers import DefaultRouter
from sock import views
from .views import SockList

# router = DefaultRouter()
# router.register(r"sock", SockList)

# urlpatterns = [
#     path("", include(router.urls))
# ]

urlpatterns = [
    path("sock/", views.SockList.as_view()),
    path("sock/<int:pk>", views.sock_detail),

]