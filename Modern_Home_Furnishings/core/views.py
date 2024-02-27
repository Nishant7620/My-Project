from django.shortcuts import render
from django.views import View
from .models import Customer,Products,Cart
from .forms import CustomerRegistrationForm
# Create your views here.

# def Home(request):    
#     return render(request,'core/home.html')         

# class base view 

class Home(View):
    def get(self,request):
        return render(request,'core/home.html')

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


class CustomerRegistrationView(View):
    def get(self,request):
        cf = CustomerRegistrationForm()
        return render(request,'core/registration.html',{'cf':cf}) 

    def post(self,request):
        cf = CustomerRegistrationForm(request.Post)
        if cf.is_valid():
            cf.save()
        return render(request,'core/registration.html',{'cf':cf})    

# def Registration(request):
#     if request.method =="POST":
#         mf = CustomerRegistrationForm(request.Post)
#         if mf.is_valid():
#             mf.save()
#         mf = CustomerRegistrationForm()    
#     else:
#         mf = CustomerRegistrationForm()


#     return render(request,'core/registration.html',{'mf':mf})    
