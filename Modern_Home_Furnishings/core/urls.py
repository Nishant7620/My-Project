from django.urls import path
from core import views

urlpatterns = [
    path('core/',views.test),
    path('us/',views.contact),
    path('a/',views.about),
    path('h/',views.Home),
]
