from django.shortcuts import render

# Create your views here.

def test(request):
    return render(request,'core/base.html')
    

def contact(request):    
    return render(request,'core/contact_us.html')

def about(request):    
    return render(request,'core/about.html')    