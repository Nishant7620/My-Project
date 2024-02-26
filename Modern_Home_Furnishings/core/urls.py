from django.urls import path
from core import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('contact_us/',views.contact),
    path('h/about/',views.about,name='x'),
    path('',views.Home.as_view(),name='home'),
    path('sofa_categories',views.Sofas.as_view(),name='sofacategories'),
    path('b/',views.beds,name='bed'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    
