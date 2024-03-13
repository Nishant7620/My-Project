from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from .models import Customer,Products,Contact,Cart,Order
from .forms import CustomerRegistrationForm,AuthenticateForm,UserProfileForm,AdminProfileForm,ChangePasswordForm,ContactForm,CustomerForm
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User

#=====================For Paypal=============================================
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.urls import reverse

#========================================================================

# Create your views here.


#-----------------class base view of Home---------------------------

class Home(View):
    def get(self,request,):
        bed_ids = [15,16,17]
        bed = Products.objects.filter(category = "BED",id__in =bed_ids)
        return render(request,'core/home.html',{'bed':bed})

def contact(request):    
    if request.method =="POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = ContactForm()        
    return render(request,'core/contact_us.html',{'form':form})


def about(request):    
    return render(request,'core/about.html')    



#-------class base view of Sofas Categories------------

class Sofas(View):
    def get(self,request):
        sofa_category = Products.objects.filter(category = 'SOFA')    # we are using filter function of queryset, that will filter those data whose category belongs to Sofa
        return render(request,'core/sofas.html',{'sofa_category':sofa_category})



#-------- class base view of Beds Categories---------------

class Beds(View):
    def get(self,request):
        Bed_category = Products.objects.filter(category = 'BED')
        return render(request,'core/beds.html',{'Bed_category':Bed_category})



class Chairs(View):
    def get(self,request):
        chair_category = Products.objects.filter(category = 'CHAIR')
        return render(request,'core/chairs.html',{'chair_category':chair_category})
#----------- class base view of Product Details--------------------------------


class ProductDetail(View):
    def get(self,request,id):
        pd = Products.objects.get(pk=id)

        #------------- code for calculate percentage -------------------------------
        if pd.discounted_price !=0:
            print(pd.discounted_price)
            percentage = int(((pd.selling_price-pd.discounted_price)/pd.selling_price)*100)

        else:
            percentage = 0
         #----------------- code end for calculate percentage ------------------------------       
        return render(request,'core/product_details.html',{'pd':pd,'percentage':percentage})


#-------------------------------Registration-------------------------------------


def CustomerRegistration(request):
    if not request.user.is_authenticated:
            if request.method == "POST":
                lf = CustomerRegistrationForm(request.POST)
                if lf.is_valid():
                    messages.success(request,'Congratulations!! Registered Successfully')    
                    lf.save()
                    return redirect('registration')
            else:
                lf = CustomerRegistrationForm()
            return render(request,'core/registration.html',{'lf':lf})
    else:
        return redirect('profile')        

#-------------------------------Login-------------------------------------

def Login(request):
    if not request.user.is_authenticated:           # check whether user is not login ,if so it will show login option
            if request.method == "POST":             # otherwise it will redirect to the profile page  
                lf = AuthenticateForm(request,request.POST)
                if lf.is_valid():
                    name = lf.cleaned_data['username']
                    pas = lf.cleaned_data['password']
                    user = authenticate(username=name,password=pas)
                    if user is not None:
                        login(request,user)
                        return redirect('/')
            else :
                lf = AuthenticateForm()
            return render(request,'core/login.html',{'lf':lf})    
    else:
        return redirect('profile') 

#-------------------------------Profile-------------------------------------

def profile(request):
    if request.user.is_authenticated:       # This check wheter user is login, if not it will redirect to login page
        if request.method =="POST":
            if request.user.is_superuser ==True:
                lf = AdminProfileForm(request.POST,instance=request.user)
            else:
                lf = UserProfileForm(request.POST,instance=request.user)
                if lf.is_valid():
                    messages.success(request, 'Congratulations!! Profile Updated Successfully.')
                    lf.save()
        else:
            if request.user.is_superuser ==True:
                lf = AdminProfileForm(instance=request.user)   
            else:
                lf = UserProfileForm(instance=request.user)
        return render(request,'core/profile.html',{'name':request.user,'lf':lf})            
    else:                                                # request.user returns the username
        return redirect('login')

#-------------------------------Logout-------------------------------------

def log_out(request):
    logout(request)
    return redirect('home')


#-------------------------------Change Password-------------------------------------

def changepassword(request):
    if request.user.is_authenticated:                # Password Change Form
        if request.method =="POST":                  # Include old password 
            lf = ChangePasswordForm(request.user,request.POST)
            if lf.is_valid():
                lf.save() 
                update_session_auth_hash(request,lf.user)
                return redirect('profile')
        else:
            lf = ChangePasswordForm(request.user,request.POST)
        return render(request,'core/changepassword.html',{'lf':lf})
    else:
        return redirect('login')    


def address(request):
 add = Customer.objects.filter(user=request.user)
 return render(request, 'core/address.html', {'add':add, 'active':'btn-primary',})


#=========================== Add TO Cart Section =================================================

def add_to_cart(request,id):                 # This 'id' is coming from 'pd.id' which hold the id of current product , which is passing through {% url 'addtocart' pd.id %} from pet_detail.html 
    if request.user.is_authenticated:
        product = Products.objects.get(pk=id)    # product variable is holding data of current object which is passed through 'id' from parameter
        user = request.user                         # user variable store the current user i.e nishant1
        Cart(user=user,product=product).save()      # In cart model current user i.e nishant1 will save in user variable and current product object will be save in product variable
        return redirect('productdetails',id)         # finally it will redirect to product_details.html with current object 'id' to display product after adding to the cart
    else:
        return redirect('login')                     # If user is not login it will redirect to login page

def view_cart(request):                                  # cart_items will fetch product of current user, and show product available in the cart of the current user.
    cart_item = Cart.objects.filter(user=request.user)
    total = 0
    delivery_charge = 2000
    for item in cart_item:
        item.product.price_and_quantity_total = item.product.selling_price * item.quantity
        total += item.product.price_and_quantity_total
    final_price = delivery_charge + total
    return render(request,'core/view_cart.html',{'cart_item':cart_item,'total':total,'final_price':final_price})


def delete_quantity(request,id):
    product = get_object_or_404(Cart,pk=id)
    if product.quantity > 1:
        product.quantity -= 1
        product.save()
    return redirect('viewcart')    

def add_quantity(request,id):                       
    product = get_object_or_404(Cart,pk=id)               # If the object is found, it returns the object. If not, it raises an HTTP 404 exception (Http404).
    product.quantity +=1                              # If object found it will be add 1 quantity to the current object   
    product.save()
    return redirect('viewcart')

def deletecart(request,id):
    if request.method=="POST":
        de = Cart.objects.get(pk=id)
        de.delete()
    return redirect('viewcart')    


#===================================== Address ============================================


def address(request):
    if request.method =="POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            user=request.user                   # user variable store the current user i.e nishant1
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            pincode = form.cleaned_data['pincode']
            Customer(user=user,name=name,address=address,city=city,state=state,pincode=pincode).save()
            return redirect('address')
            
    else:           
        form = CustomerForm()
    address = Customer.objects.filter(user=request.user) 
    return render(request,'core/address.html',{'form':form,'address':address})  


def deleteaddress(request,id):
    if request.method =='POST':
        de =Customer.objects.get(pk=id)
        de.delete()
    return redirect('address')


#===================================== Checkout ============================================

def checkout(request):

    cart_item = Cart.objects.filter(user=request.user)      # cart_items will fetch product of current user, and show product available in the cart of the current user.
    total = 0
    delivery_charge = 2000
    for item in cart_item:
        item.product.price_and_quantity_total = item.product.selling_price * item.quantity
        total += item.product.price_and_quantity_total
    final_price = delivery_charge + total

    address = Customer.objects.filter(user=request.user)
    return render(request,'core/checkout.html',{'cart_item':cart_item,'total':total,'final_price':final_price,'address':address})

#===================================== Payment ============================================

# def payment(request):

#     if request.method=="POST":
#         selected_address_id = request.POST.get('selected_address') 

#     cart_item = Cart.objects.filter(user=request.user)            # cart_items will fetch product of current user, and show product available in the cart of the current user.
#     total = 0
#     delivery_charge = 2000
#     for item in cart_item:
#         item.product.price_and_quantity_total = item.product.selling_price * item.quantity
#         total += item.product.price_and_quantity_total
#     final_price = delivery_charge + total

#     address = Customer.objects.filter(user=request.user)

# #================================ Paypal code ===============================================

#     host = request.get_host()    # Will fecth the domain site is currently hosted on.

#     paypal_checkout = {
#         'business':settings.PAYPAL_RECEIVER_EMAIL,
#         'amount':final_price,
#         'item_name':'Product',
#         'invoice':uuid.uuid4(),
#         'currency_code':'USD',
#         'notify_url':f"http://{host}{reverse('paypal-ipn')}",
#         'return_url':f"http://{host}{reverse('paymentsuccess',args=[selected_address_id])}",
#         'cancel_url':f"http://{host}{reverse('paymentfailed')}",
#     }
    
#     paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

# #======================================================================================


#     return render(request,'core/payment.html',{'cart_item':cart_item,'total':total,'final_price':final_price,'address':address,'paypal_payment':paypal_payment})




def payment(request):
    if request.method == "POST":
        selected_address_id = request.POST.get('selected_address')
        if selected_address_id is None:
            return redirect('checkout')
        request.session['selected_address_id'] = selected_address_id
        return redirect('payment')

    selected_address_id = request.session.get('selected_address_id')

    cart_item = Cart.objects.filter(user=request.user)
    total = 0
    delivery_charge = 2000
    for item in cart_item:
        item.product.price_and_quantity_total = item.product.selling_price * item.quantity
        total += item.product.price_and_quantity_total
    final_price = delivery_charge + total

    address = Customer.objects.filter(user=request.user)

    host = request.get_host()

    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': final_price,
        'item_name': 'Product',
        'invoice': uuid.uuid4(),
        'currency_code': 'USD',
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",
        'return_url': f"http://{host}{reverse('paymentsuccess', args=[selected_address_id])}",
        'cancel_url': f"http://{host}{reverse('paymentfailed')}",
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

    return render(request, 'core/payment.html', {'cart_item': cart_item, 'total': total, 'final_price': final_price, 'address': address, 'paypal_payment': paypal_payment})

#===================================== Payment Success ============================================

def payment_success(request,selected_address_id):                    # we have fetch this id from return_url': f"http://{host}{reverse('paymentsuccess', args=[selected_address_id])}
    user =request.user                                                  # This id contain address detail of particular customer
    customer_data = Customer.objects.get(pk=selected_address_id)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        Order(user=user,customer = customer_data,product=c.product,quantity=c.quantity).save()
        c.delete()
    return render(request,'core/payment_successful.html')


#===================================== Payment Failed ============================================

def payment_failed(request):
    return render(request,'core/payment_failed.html')    


#===================================== Order ====================================================

def order(request):
    ordr =Order.objects.filter(user=request.user)
    return render(request,'core/order.html',{'ordr':ordr})
    

#========================================== Buy Now ================================================    

def buynow(request,id):
    product = Products.objects.get(pk=id)     # cart_items will fetch product of current user, and show product available in the cart of the current user.
    delhivery_charge =2000
    final_price= delhivery_charge + product.selling_price
    
    address = Customer.objects.filter(user=request.user)

    return render(request, 'core/buynow.html', {'final_price':final_price,'address':address,'product':product})


def buynow_payment(request,id):

    if request.method == 'POST':
        selected_address_id = request.POST.get('buynow_selected_address')

    product = Products.objects.get(pk=id)     # cart_items will fetch product of current user, and show product available in the cart of the current user.
    delhivery_charge =2000
    final_price= delhivery_charge + product.selling_price
    
    address = Customer.objects.filter(user=request.user)
    #================= Paypal Code ======================================

    host = request.get_host()   # Will fecth the domain site is currently hosted on.

    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': final_price,
        'item_name': 'Product',
        'invoice': uuid.uuid4(),
        'currency_code': 'USD',
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",
        'return_url': f"http://{host}{reverse('buynowpaymentsuccess', args=[selected_address_id,id])}",
        'cancel_url': f"http://{host}{reverse('paymentfailed')}",
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

    #========================================================================

    return render(request, 'core/payment.html', {'final_price':final_price,'address':address,'product':product,'paypal_payment':paypal_payment})

def buynow_payment_success(request,selected_address_id,id):
    print('payment sucess',selected_address_id)   # we have fetch this id from return_url': f"http://{host}{reverse('paymentsuccess', args=[selected_address_id])}
                                                  # This id contain address detail of particular customer
    user =request.user
    customer_data = Customer.objects.get(pk=selected_address_id,)
    
    product = Products.objects.get(pk=id)
    Order(user=user,customer=customer_data,product=product,quantity=1).save()
   
    return render(request,'core/buynow_payment_success.html')