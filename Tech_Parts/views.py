from django.shortcuts import render,redirect,reverse
from django.shortcuts import get_object_or_404
from .models import *
from .filters import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.



def home(request):
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

def product(request):    
    if request.user.is_authenticated:
        if Filters.objects.filter(customer_id=request.user.id).exists():
            filter=Filters.objects.get(customer_id=request.user.id)
            product=Product.objects.filter(category=filter.category,processor=filter.processor,type=filter.type)
        else:
            messages.error(request,"you dont have order yet")
            return redirect(reverse("home:home"))
    else:   
        filter=Filters.objects.filter(device=request.COOKIES["device"])
        if filter.exists():
            my_filter=Filters.objects.get(device=request.COOKIES["device"])
            product=Product.objects.filter(category=my_filter.category,processor=my_filter.processor,type=my_filter.type)
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
                    print("here")     
                # # instance.save()   
                # print("saved")
            else:
                Order.objects.create(customer=customer,ordered=True,delivered=False)
                for i in order:
                    i.products.set(form.cleaned_data.get("products"))
                    i.save()
                    print("created") 
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
                    # # instance.save()   
                    # print("saved")
                else:    
                    Order.objects.create(device=request.COOKIES['device'],ordered=True,delivered=False)
                    for i in order:
                        i.products.set(form.cleaned_data.get("products"))
                        i.save()
                        print("created") 
                  
            else:
                messages.success(request,"you dont have order yet")
                return redirect(reverse("hme:home"))
    context={"products":product}  
    return render(request,"products.html",context)
@login_required
def dashboard(request):
    if request.user.is_superuser:
        form=DashboardForm(request.POST or None,request.FILES or None)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.save()
            messages.success(request,"Product added Successfully")
            return redirect(reverse("home:home"))
    else:
        messages.error(request,"you dont have permission to add products")
        return redirect(reverse("home:home"))
    context={"form":form}
    return render(request,"dashboard.html",context)
   