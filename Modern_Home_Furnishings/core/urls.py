from django.urls import path
from core import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('contact_us/',views.contact),
    path('h/about/',views.about,name='x'),
    path('',views.Home.as_view(),name='home'),
    path('sofa_categories',views.Sofas.as_view(),name='sofacategories'),
    path('bed_categories',views.Beds.as_view(),name='bedcategories'),
    path('product_details/<int:id>/',views.ProductDetail.as_view(),name='productdetails'),
    path('registration',views.CustomerRegistration,name='registration'),
    path('login',views.Login,name='login'),
    path('profile',views.profile,name='profile'),
    path('logout',views.log_out,name='logout'),
    path('changepassword',views.changepassword,name='changepassword')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    
