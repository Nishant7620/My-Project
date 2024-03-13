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
    path('chair_categories',views.Chairs.as_view(),name='chaircategories'),
    path('product_details/<int:id>/',views.ProductDetail.as_view(),name='productdetails'),
    path('registration',views.CustomerRegistration,name='registration'),
    path('login',views.Login,name='login'),
    path('profile',views.profile,name='profile'),
    path('logout',views.log_out,name='logout'),
    path('changepassword',views.changepassword,name='changepassword'),
    path('add_to_cart/<int:id>/',views.add_to_cart,name='addtocart'),
    path('viewcart',views.view_cart,name='viewcart'),
    path('delete_quantity/<int:id>/',views.delete_quantity,name='delete_quantity'),
    path('add_quantity/<int:id>/',views.add_quantity,name='add_quantity'),
    path('deletecart/<int:id>/',views.deletecart,name='deletecart'),
    path('address/',views.address,name='address'),
    path('deleteaddress/<int:id>/',views.deleteaddress,name='deleteaddress'),
    path('checkout/',views.checkout,name='checkout'),
    path('payment/',views.payment,name='payment'),
    path('payment_success/<int:selected_address_id>',views.payment_success,name='paymentsuccess'),
    path('payment_failed/',views.payment_failed,name='paymentfailed'),
    path('order/',views.order,name='order'),
    path('buynow/<int:id>',views.buynow,name='buynow'),
    path('buynow_payment/<int:id>/',views.buynow_payment,name='buynowpayment'),
    path('buynow_payment_success/<int:selected_address_id>/<int:id>',views.buynow_payment_success,name='buynowpaymentsuccess')
   
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    
