from django.urls import path
from core import views

urlpatterns = [
    path('core/',views.test),
    path('contact_us/',views.contact),
    path('h/about/',views.about,name='x'),
    path('h/',views.Home,name='home'),
    path('s/',views.sofas,name='sofa'),
    path('b/',views.beds,name='bed'),
]
