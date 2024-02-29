from django.shortcuts import render,redirect
from django.views import View
from .models import Customer,Products,Cart
from .forms import CustomerRegistrationForm,AuthenticateForm,UserProfileForm,AdminProfileForm,ChangePasswordForm
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
# Create your views here.

# def Home(request):    
#     return render(request,'core/home.html')         

# class base view 

class Home(View):
    def get(self,request):
        Bed_category = Products.objects.filter(category = 'BED')
        return render(request,'core/home.html',{'Bed_category':Bed_category})

def contact(request):    
    return render(request,'core/contact_us.html')

def about(request):    
    return render(request,'core/about.html')    



# def sofas(request):    
#     return render(request,'core/sofas.html') 

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
                lf.save()
        else:
            if request.user.is_superuser ==True:
                lf = AdminProfileForm(instance=request.user)   
            else:
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




