from django.shortcuts import render
from django.views import View
from .models import Customer,Products,Cart
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

def beds(request):    
    return render(request,'core/beds.html')            