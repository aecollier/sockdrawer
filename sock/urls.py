from django.urls import path, include
from rest_framework.routers import DefaultRouter
from sock import views
from .views import SockList
#from .views import PairsList

# router = DefaultRouter()
# router.register(r"sock", SockList)

# urlpatterns = [
#     path("", include(router.urls))
# ]

urlpatterns = [
    path("sock/", views.SockList.as_view()),
    path("sock/<int:id>", views.sock_detail),
    path("sock/<int:id>/", views.sock_detail),
    #path("pairs/", views.PairsList.as_view()),
    path("pairs/", views.pair_list),

]