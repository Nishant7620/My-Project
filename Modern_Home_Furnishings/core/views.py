from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from .models import Customer,Products,Contact,Cart
from .forms import CustomerRegistrationForm,AuthenticateForm,UserProfileForm,AdminProfileForm,ChangePasswordForm,ContactForm
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User
# Create your views here.

# def Home(request):    
#     return render(request,'core/home.html')         

# class base view 

class Home(View):
    def get(self,request,):
        bed_ids = [15,16,17]
        bed = Products.objects.filter(category = "BED",id__in =bed_ids)
        return render(request,'core/home.html',{'bed':bed})

def contact(request):
    # form = ContactForm()   
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



#class base view of Sofas Categories

class Sofas(View):
    def get(self,request):
        sofa_category = Products.objects.filter(category = 'SOFA')    # we are using filter function of queryset, that will filter those data whose category belongs to Sofa
        return render(request,'core/sofas.html',{'sofa_category':sofa_category})



# class base view of Beds Categories

class Beds(View):
    def get(self,request):
        Bed_category = Products.objects.filter(category = 'BED')
        return render(request,'core/beds.html',{'Bed_category':Bed_category})


# class base view of Product Details


class ProductDetail(View):
    def get(self,request,id):
        product_detail = Products.objects.get(pk=id)
        return render(request,'core/product_details.html',{'pd':product_detail})


#-----------------------------------------------------------------------------


# class CustomerRegistrationView(View):
#     def get(self,request):
#         cf = CustomerRegistrationForm()
#         return render(request,'core/registration.html',{'cf':cf}) 

#     def post(self,request):
#         if not request.user.is_authenticated:
#             if request.method == "POST":
#                 cf = CustomerRegistrationForm(request.POST)
#                 if cf.is_valid():
#                     cf.save()
#                 return redirect('registration')
#         else:
#             return redirect('profile')    

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


# class LoginView(View):
#     def get(self,request):
#         lf = AuthenticateForm()
#         return render(request,'core/login.html',{'lf':lf})

#     def post(self,request):
#         if not request.user.is_authenticated:
#             if request.method == "POST":
#                 lf = AuthenticateForm(request,request.POST)
#                 if lf.is_valid():
#                     name = lf.cleaned_data['username']
#                     pas = lf.cleaned_data['password']
#                     user = authenticate(username=name,password=pas)
#                     if user is not None:
#                         login(request,user)
#                         return redirect('/')
#             else :
#                 lf = AuthenticateForm()
#             return render(request,'core/login.html',{'lf':lf})    
#         else:
#             return redirect('profile')           


def Login(request):
    if not request.user.is_authenticated:
            if request.method == "POST":
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


def profile(request):
    if request.user.is_authenticated:
        if request.method =="POST":
            if request.user.is_superuser ==True:
                lf = AdminProfileForm(request.POST,instance=request.user)
            else:
                lf = UserProfileForm(request.POST,instance=request.user)
                if lf.is_valid():
                    usr = request.user
                    name = lf.cleaned_data['name']
                    address = lf.cleaned_data['address']
                    city = lf.cleaned_data['city']
                    state = lf.cleaned_data['state']
                    pincode = lf.cleaned_data['pincode']
                    reg = Customer(user=usr, name=name, address=address, city=city, state=state, pincode=pincode)
                    reg.save()
                    messages.success(request, 'Congratulations!! Profile Updated Successfully.')
                    lf.save()
        else:
            if request.user.is_superuser ==True:
                lf = AdminProfileForm(instance=request.user)   
            else:

                # info =Customer.objects.get(user=request.user)
                lf = UserProfileForm(instance=request.user)
        return render(request,'core/profile.html',{'name':request.user,'lf':lf})            
    else:
        return redirect('login')


def log_out(request):
    logout(request)
    return redirect('home')

def changepassword(request):
    if request.user.is_authenticated:
        if request.method =="POST":
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


def add_to_cart(request,id):
    if request.user.is_authenticated:
        product = Products.objects.get(pk=id)
        user = request.user
        Cart(user=user,product=product).save()
        return redirect('productdetails', id)
    else:
        return redirect('login')    

def view_cart(request):
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
    print(id)
    product = get_object_or_404(Cart,pk=id)
    product.quantity +=1
    product.save()
    return redirect('viewcart')

def deletecart(request,id):
    if request.method=="POST":
        de = Cart.objects.get(pk=id)
        de.delete()
    return redirect('viewcart')    