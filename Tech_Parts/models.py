from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render,redirect,reverse

from django.db.models.fields.related import ForeignObject
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from tinymce.models import HTMLField
# Create your models here.

class Type(models.Model):
    name=models.CharField(max_length=50)
    li=models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        slug=self.name
        return reverse("home:category",kwargs={"slug":slug})
class Category(models.Model):
    name=models.CharField(max_length=50)
       
    def __str__(self):
        return str(self.name)  
    
    def get_absolute_url(request,self):
        name=request.user
        slug= name 
        return name
    
class Processor(models.Model):
    name=models.CharField(max_length=50)
    image=models.CharField(max_length=3000)
    def __str__(self):
        return self.name      

@receiver(post_save, sender=User)   
def create_user_Customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(name=instance)
        
class Customer(models.Model):
    device=models.CharField(max_length=120,blank=True,null=True)
    name=models.OneToOneField(User,default=1,on_delete=models.CASCADE)          
    category=models.ForeignKey(Category,null=True,on_delete=models.SET_NULL)  
    email=models.EmailField(max_length=50)
    phone=models.CharField(max_length=11)
    
    def __str__(self):
        return self.name.username
    
class Supplier(models.Model): 
    name=models.CharField(max_length=50)
    image=models.ImageField()
    phone=models.CharField(max_length=11)
    # email=models.EmailField(max_length=100)
    address=models.CharField(max_length=120)
    location=models.CharField(max_length=120)
    def __str__(self):
        return self.name
class Product_Filter(models.Model):
    name=models.CharField(max_length=50)
    def __str__(self):
        return self.name
class Product(models.Model):
    name=models.CharField(max_length=100)
    filter=models.ForeignKey(Product_Filter,default=1,on_delete=models.CASCADE)
    image=models.CharField(max_length=3000)
    price=models.PositiveIntegerField(default=0)
    category=models.ForeignKey(Category,default=1,null=True,on_delete=models.SET_NULL)
    processor=models.ManyToManyField(Processor)
    type=models.ForeignKey(Type,default=6,null=True,on_delete=models.SET_NULL)
    
    details=HTMLField() 
    code=models.CharField(max_length=100,blank=True)
    slug=models.SlugField(blank=True,max_length=100,unique=True)
    date_modified=models.DateTimeField(auto_now=True)    
  
    def __str__(self):  
        return self.name      
    
    def discount(self):
        price=(10/100)*self.price   
        return price 
    def total_price(self): 
        price=self.price - self.discount()
        return price
    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
    
class Filters(models.Model):
    type=models.ForeignKey(Type,blank=True,null=True,on_delete=models.CASCADE)
    processor=models.ManyToManyField(Processor,blank=True)
    category=models.ForeignKey(Category,blank=True,null=True,on_delete=models.CASCADE)
    device=models.CharField(max_length=120,blank=True,null=True)
    customer=models.ForeignKey(Customer,null=True,blank=True,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id)
      
class Games(models.Model):
    name=models.CharField(max_length=50)
    gamer_high_end=models.PositiveIntegerField(default=0)
    gamer_medium=models.PositiveIntegerField(default=0)
    gamer_low_end=models.PositiveIntegerField(default=0)
    li=models.CharField(max_length=100)
    def __str__(self):
        return self.name
import random

    
class Fps_Numbers(models.Model):
    category=models.ForeignKey(Category,default=1,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    details=models.CharField(max_length=50)
    value=models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.name
class Order(models.Model):
    customer=models.ForeignKey(Customer,blank=True,null=True,on_delete=models.CASCADE)   
    # supplier=models.ForeignKey(Supplier,on_delete=models.CASCADE,default=1) 
    products=models.ManyToManyField(Product,blank=True)
    code=models.CharField(blank=True,null=True,max_length=100)
    ordered=models.BooleanField(default=False)
    delivered=models.BooleanField(default=False)
    device=models.CharField(max_length=120,blank=True,null=True)
    def __str__(self):
        return str(self.id)
    
    def total_price(self):
        price=0
        for i in self.products.all():
            price += i.price
            
        return price

    def discount(self):
        percentage=(10/100)*self.total_price()
        return percentage
            # disc=0
            # for i in self.products.all():
            #     price +=i.    
            
    def after_price(self):
        price= self.total_price() - self.discount()
        return price
    
    def save(self, *args, **kwargs): # new
        if not self.code: 
            num=random.random()
            self.code =str(num) + "-2021"
        return super().save(*args, **kwargs) 
              
# class Account(models.Model):
#     code=models.ForeignKey(Order,on_delete=models.CASCADE)
#     invoice=models.PositiveIntegerField(blank=True,null=True)
#     supplier=models.ForeignKey(Supplier,on_delete=models.CASCADE)
    
#     def __Str__(self):
#         return (f"{self.supplier.name} account")
    
    
    