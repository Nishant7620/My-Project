from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Customer(models.Model):

    STATE_CHOICES = [
        ('AP', 'Andhra Pradesh'),
        ('AR', 'Arunachal Pradesh'),
        ('AS', 'Assam'),
        ('BR', 'Bihar'),
        ('CT', 'Chhattisgarh'),
        ('GA', 'Goa'),
        ('GJ', 'Gujarat'),
        ('HR', 'Haryana'),
        ('HP', 'Himachal Pradesh'),
        ('JH', 'Jharkhand'),
        ('KA', 'Karnataka'),
        ('KL', 'Kerala'),
        ('MP', 'Madhya Pradesh'),
        ('MH', 'Maharashtra'),
        ('MN', 'Manipur'),
        ('ML', 'Meghalaya'),
        ('MZ', 'Mizoram'),
        ('NL', 'Nagaland'),
        ('OR', 'Odisha'),
        ('PB', 'Punjab'),
        ('RJ', 'Rajasthan'),
        ('SK', 'Sikkim'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # we have created Many-to-one relationship i.e multiple order can be done by one user
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2, choices=STATE_CHOICES)
    pincode = models.IntegerField(
    default= 0,
    blank= True,
    null= True
    )

 
 

class Products(models.Model):

    CATAGORY_CHOICES = [
        ('SOFA','Sofa'),
        ('BED','Bed'),
        ('CHAIR','Chair'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20,choices=CATAGORY_CHOICES)
    small_description = models.TextField()
    description = models.TextField()
    selling_price = models.IntegerField()
    discounted_price = models.IntegerField(default=0)
    percentage = models.IntegerField(default=0)
    price_and_quantity_total = models.IntegerField(default=0)
    product_image = models.ImageField(upload_to = 'product_images',default='none')   # As we are using image field we have to intall 'pillow'. And we have to Define MEDIA_URL in settings.py file so that all folder should save in media directory

    def __str__(self):
        return str(self.id)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)            #Each cart instance is associated with a single user. 
    product = models.ForeignKey(Products,on_delete=models.CASCADE)       #Each cart instance is associated with a single Product product. Similarly, the on_delete=models.CASCADE argument means that if the referenced product object is deleted, the corresponding Cart instances associated with that product will be deleted.
    quantity = models.PositiveIntegerField(default=1)           # Quantity cannot be negative so we have used PositiveIntegerField

    def __str__(self):
        return str(self.id)

class Order(models.Model):

    STATUS_CHOICES = [
        ('PENDING','Pending'),
        ('PROCESSING','Processing'),
        ('COMPLETED','Completed'),
        ('CANCELLED','Cancelled')

    ]   

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,default=None)   
    product = models.ForeignKey(Products,on_delete=models.CASCADE) 
    quantity =models.PositiveIntegerField(default = 1)
    order_at =models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,default='PENDING')
   

    def __str__(self):
        return str(self.id)
        

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    message = models.CharField(max_length=100)
    