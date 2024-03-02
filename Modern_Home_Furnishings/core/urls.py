from django.urls import path
from core import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('contact_us/',views.contact,name='contact'),
    path('h/about/',views.about,name='about'),
    path('',views.Home.as_view(),name='home'),
    path('sofa_categories',views.Sofas.as_view(),name='sofacategories'),
    path('bed_categories',views.Beds.as_view(),name='bedcategories'),
    path('product_details/<int:id>/',views.ProductDetail.as_view(),name='productdetails'),
    path('registration',views.CustomerRegistration,name='registration'),
    path('login',views.Login,name='login'),
    path('profile',views.profile,name='profile'),
    path('address/', views.address, name='address'),
    path('logout',views.log_out,name='logout'),
    path('changepassword',views.changepassword,name='changepassword'),
    path('add_to_cart/<int:id>/',views.add_to_cart,name='addtocart'),
    path('viewcart',views.view_cart,name='viewcart')
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    
