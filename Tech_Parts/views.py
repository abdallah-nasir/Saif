from django.shortcuts import render,redirect,reverse
from django.shortcuts import get_object_or_404
from django.conf import settings
from .models import *
from .filters import *
from .forms import *
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
# Create your views here.
import json
      

def home(request):
    # gammes=Gammes.objects.get(name="GTA V")
    # gammes.gammer_high_end,gammes.gammer_medium,gammes.gammer_low_end=[76,2,3]
    # gammes.save()   
    # print("DONE")
        
    type=Type.objects.all()
    form=TypeFilter(request.POST or None)
    if form.is_valid():
      
        if request.user.is_authenticated:
            my_filter=Filters.objects.filter(customer_id=request.user.id)
            if my_filter.exists():
                my_filter=Filters.objects.get(customer_id=request.user.id)
                my_filter.type=form.cleaned_data.get("type")
                my_filter.save()  
                messages.success(request,f"you choosed '{my_filter.type}'")  
                return redirect(reverse("home:category"))
            else:    
                Filters.objects.create(customer_id=request.user.id,type=form.cleaned_data.get("type"))
                messages.success(request,f" you choosed '{form.cleaned_data.get('type')}'")
                return redirect(reverse("home:category"))
        else:
            if Filters.objects.filter(device=request.COOKIES["device"]).exists():
                my_filter=Filters.objects.get(device=request.COOKIES["device"])
                my_filter.type=form.cleaned_data.get("type")
                my_filter.save()  
                messages.success(request,f"you choosed '{my_filter.type}'")
                return redirect(reverse("home:category"))
            else:    
                Filters.objects.create(device=request.COOKIES["device"],type=form.cleaned_data.get("type"))
                messages.success(request,f"you choosed '{form.cleaned_data.get('type')}'")
                return redirect(reverse("home:category"))

    context={"type":type,"form":form}
    return render(request,"index.html",context)
   
def category(request):
    category=Category.objects.all()  
    form=CategoryFilter(request.POST or None)
    if form.is_valid():
        if request.user.is_authenticated:
            if Filters.objects.filter(customer_id=request.user.id).exists():
                my_filter=Filters.objects.get(customer_id=request.user.id)
               
                my_filter.category=form.cleaned_data.get("category")
                my_filter.save()
                messages.success(request,f"you choosed '{my_filter.category}'")
                return redirect(reverse("home:processor"))
            else:    
                Filters.objects.create(customer_id=request.user.id,category=form.cleaned_data.get("category"))
                messages.success(request,f"you choosed '{form.cleaned_data.get('category')}'")
                return redirect(reverse("home:processor"))
        else:
            if Filters.objects.filter(device=request.COOKIES["device"]).exists():
                my_filter=Filters.objects.get(device=request.COOKIES["device"])
                my_filter.category=form.cleaned_data.get("category")
                my_filter.save()
                messages.success(request,f"you choosed '{my_filter.category}'")
                return redirect(reverse("home:processor"))
            else:    
                Filters.objects.create(device=request.COOKIES["device"],category=form.cleaned_data.get("category"))
                messages.success(request,f"you choosed '{form.cleaned_data.get('category')}'")

                return redirect(reverse("home:processor"))    
    context={"categories":category}
    return render(request,"gaming1.html",context)

def processor(request):
    processor=Processor.objects.all()
    form=ProcessorFilter(request.POST or None)
    if form.is_valid():
        if request.user.is_authenticated:
            if Filters.objects.filter(customer_id=request.user.id).exists():
                my_filter=Filters.objects.get(customer_id=request.user.id)
               
                my_filter.processor=form.cleaned_data.get("processor")
                my_filter.save()
                messages.success(request,"Products mathches with your choice")
                return redirect(reverse("home:product"))

            else:    
                Filters.objects.create(customer_id=request.user.id,processor=form.cleaned_data.get("processor"))
                messages.success(request,"Products mathches with your choice")
                return redirect(reverse("home:product"))
        else: 
            if Filters.objects.filter(device=request.COOKIES["device"]).exists():
                my_filter=Filters.objects.get(device=request.COOKIES["device"])
                my_filter.processor=form.cleaned_data.get("processor")
                my_filter.save()
                messages.success(request,"Products mathches with your choice")
                return redirect(reverse("home:product"))
            else:    
                Filters.objects.create(device=request.COOKIES["device"],processor=form.cleaned_data.get("processor"))
                messages.success(request,"Products mathches with your choice")
                return redirect(reverse("home:product")) 
    context={"processor":processor}
    return render(request,"type.html",context)
from django.core.paginator import Paginator
def product(request):  
    # a=Product.objects.get(id=6)  
    # print(a)
    if request.user.is_authenticated:
        if Filters.objects.filter(customer_id=request.user.id).exists():
            filter=Filters.objects.get(customer_id=request.user.id)
            product=Product.objects.filter(category=filter.category,processor=filter.processor) | Product.objects.all()[0:11]
            paginator = Paginator(product,6) # Show 6 contacts per page.

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            # product=Product.objects.all()[0:10]   
        else:
            messages.error(request,"you dont have order yet")   
            return redirect(reverse("home:home"))
    else:   
        filter=Filters.objects.filter(device=request.COOKIES["device"])
        if filter.exists():
            my_filter=Filters.objects.get(device=request.COOKIES["device"])
            product=Product.objects.filter(category=my_filter.category,processor=my_filter.processor) | Product.objects.all()[0:11]
            paginator = Paginator(product,6) # Show 25 contacts per page.

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)        
        else:
            messages.error(request,"you dont have order yet")
            return redirect(reverse("home:home"))   
    form=OrderForm(request.POST or None)
    if form.is_valid():
        instance=form.save(commit=False)
        if request.user.is_authenticated:  
            customer=Customer.objects.get(name=request.user)
            order=Order.objects.filter(customer=customer,ordered=True,delivered=False)
            if order.exists():
                print(form.cleaned_data.get("products"))
                for i in order:  
                    i.products.set(form.cleaned_data.get("products"))
                    i.save()
                return redirect(reverse("home:result"))
            else:
                Order.objects.create(customer=customer,ordered=True,delivered=False)
                for i in order:
                    i.products.set(form.cleaned_data.get("products"))
                    i.save()
                return redirect(reverse("home:result")) 
        else:
            if Filters.objects.filter(device=request.COOKIES["device"]).exists():
                # my_customer=Customer.objects.get(device=request.COOKIES["device"])
                order=Order.objects.filter(device=request.COOKIES["device"],ordered=True,delivered=False)
                if order.exists():
                    # print(form.cleaned_data.get("products"))
                    for i in order:  
                        i.products.set(form.cleaned_data.get("products"))
                        i.save()
                        print("here")     
                    return redirect(reverse("home:result"))
                else:    
                    Order.objects.create(device=request.COOKIES['device'],ordered=True,delivered=False)
                    for i in order:
                        i.products.set(form.cleaned_data.get("products"))
                        i.save()
                    return redirect(reverse("home:result"))
                  
            else:
                messages.error(request,"you dont have order yet")
                return redirect(reverse("hme:home"))
    context={"products":page_obj}   
    return render(request,"products.html",context)

def result(request):  
    gammes=Gammes.objects.all() 
   
    if request.user.is_authenticated:
        order=Order.objects.filter(customer_id=request.user.id,ordered=True,delivered=False)
        filter=Filters.objects.filter(customer_id=request.user.id) 
        if filter.exists():
            my_filter=Filters.objects.get(customer_id=request.user.id)
            
        else:
            messages.error(request,"toy don't have order yet")
            return redirect(reverse("home:home")) 
        if order.exists():
            my_order=Order.objects.get(customer_id=request.user.id,ordered=True,delivered=False)
        else:
            messages.error(request,"toy don't have order yet")
            return redirect(reverse("home:home"))
        if request.method == "POST":   
            supplier=Supplier.objects.all()[0]
            edit_filter=Filters.objects.get(customer_id=request.user.id)
            edit_filter.type,edit_filter.processor, edit_filter.category = None,None,None
            edit_filter.save()  
            my_order.delivered=True
            my_order.save()   
            send_mail(       
                "Payment Completed",  
                f"you have completed a Payment Transaction,\n your code : {my_order.code} \n supplier name : {supplier.name} \n supplier phone : {supplier.phone} \n location : {supplier.address}",
                settings.EMAIL_HOST_USER,
            [request.user.email,],
                fail_silently =False
            )
            print("DONE")   
            # supllier=Supplier.objects.all()[0]
               
               
      
    else:   
        order=Order.objects.filter(device=request.COOKIES["device"],ordered=True,delivered=False)
        filter=Filters.objects.filter(device=request.COOKIES["device"])
        if filter.exists():
            my_filter=Filters.objects.get(device=request.COOKIES["device"])
        else:
            messages.error(request,"toy don't have order yet")
            return redirect(reverse("home:home")) 
        if order.exists():
            my_order=Order.objects.get(device=request.COOKIES["device"],ordered=True,delivered=False)
        else:
            messages.error(request,"toy don't have order yet")
            return redirect(reverse("home:home"))

    context={"orders":my_order,"filters":my_filter,"gammes":gammes} 
    return render(request,"result.html",context)


@login_required
def dashboard(request):    
    products=Product.objects.all().order_by("-id")
    if request.user.is_superuser:
        print("hi")
        # if request.method =="POST":
            
        #     messages.success(request,"Product added Successfully")
        #     return redirect(reverse("home:home"))
    else:
        messages.error(request,"you dont have permission to add products")
        return redirect(reverse("home:home"))
    context={"products":products}
    return render(request,"dashboard/index.html",context)

def add(request):
    form =DashboardForm(request.POST or None ,request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request,"Product added successfully")
        return redirect(reverse("home:dashboard"))
    context={"form":form}
    return render(request,"dashboard/add.html",context)
       
def edit(request,slug):
    product=get_object_or_404(Product,slug=slug)
    form =DashboardForm(request.POST or None ,request.FILES or None,instance=product)
    if form.is_valid():
        form.save()
        messages.success(request,"Product updated successfully")
        return redirect(reverse("home:dashboard"))
    context={"form":form,"product":product}
    return render(request,"dashboard/edit.html",context)
       
def delete(request,slug):
    product=get_object_or_404(Product,slug=slug)
    
    product.delete()
    messages.success(request,"product deleted successfully")
    return redirect(reverse("home:dashboard"))   
    # return render(request,"dashboard/index.html")   
    
def profile(request):
    order=Order.objects.filter(customer_id=request.user.id,ordered=True,delivered=True)
    context={"order":order}
    return render(request,"dashboard/profile.html",context)  
    # return render(request,"dashboard/index.html")   
    
def supplier(request):
    form=SupplierForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request,"you added supplier")
        return redirect(reverse("home:dashboard"))
    context={"form":form}
   
    return render(request,"dashboard/supplier.html",context)   
             