from django.urls import path
from . import views

urlpatterns = [
    path("",views.home,name="home"),
    path("get-route",views.get_route,name="get-route"),
    path("preview",views.preview,name="preview")
]
