from django.urls import path
from core import views

urlpatterns = [
    path('core/',views.test),
    path('contact_us/',views.contact),
    path('h/about/',views.about),
    path('h/',views.Home),
    path('s/',views.sofas),
    path('b/',views.beds),
]
