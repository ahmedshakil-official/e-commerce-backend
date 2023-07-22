from django.urls import path
from . import views
# import debug_toolbar

urlpatterns = [

    path('', views.home),
]