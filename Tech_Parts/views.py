from django.shortcuts import render,redirect,reverse
from django.shortcuts import get_object_or_404
from django.conf import settings
from .models import *
from .filters import *
from .forms import *
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
# Create your views here.
import json
      
    


def home(request):
    # msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
    # msg.attach_file('templates/index.html')
    # msg.content_subtype = "html"  
    # msg.send()        
    type=Type.objects.all().order_by("id")
    form=TypeFilter(request.POST or None)
    if form.is_valid():
      
        if request.user.is_authenticated:
            my_filter=Filters.objects.filter(customer_id=request.user.id)
            if my_filter.exists():
                my_filter=Filters.objects.get(customer_id=request.user.id)
                my_filter.type=form.cleaned_data.get("type")
                my_filter.save()  
                if my_filter.type.name == "Normal":
                    messages.success(request,f" products mathces with your choice ")
                    return redirect(reverse("home:product"))
                else:
                    messages.success(request,f"you choosed '{my_filter.type}'")  
                    return redirect(reverse("home:category"))
            else:    
                Filters.objects.create(customer_id=request.user.id,type=form.cleaned_data.get("type"))
                my_filter=Filters.objects.get(customer_id=request.user.id)
                if my_filter.type.name == "Normal":
                    messages.success(request,f" products mathces with your choice ")
                    return redirect(reverse("home:product"))    
                else:            
                    messages.success(request,f" you choosed '{form.cleaned_data.get('type')}'")
                    return redirect(reverse("home:category"))
        else:
            if Filters.objects.filter(device=request.COOKIES["device"]).exists():
                my_filter=Filters.objects.get(device=request.COOKIES["device"])
                my_filter.type=form.cleaned_data.get("type")
                my_filter.save()  
                if my_filter.type.name == "Normal":
                    messages.success(request,f" products mathces with your choice ")
                    return redirect(reverse("home:product"))
                else:
                    messages.success(request,f"you choosed '{my_filter.type}'")
                    return redirect(reverse("home:category"))
            else:    
                Filters.objects.create(device=request.COOKIES["device"],type=form.cleaned_data.get("type"))
                my_filter=Filters.objects.get(device=request.COOKIES["device"])
                if my_filter.type.name == "Normal":
                    messages.success(request,f" products mathces with your choice ")
                    return redirect(reverse("home:product"))
                else:
                    messages.success(request,f"you choosed '{my_filter.type}'")
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
                for i in Filters.objects.filter(customer_id=request.user.id):
              
                    i.processor.set(request.POST.get("processor"))
                    i.save()   
                messages.success(request,"Products mathches with your choice")
                return redirect(reverse("home:product"))
    
            else:  
                Filters.objects.create(customer_id=request.user.id,processor=form.cleaned_data.get("processor"))
                messages.success(request,"Products mathches with your choice")
                return redirect(reverse("home:product"))
        else: 
            if Filters.objects.filter(device=request.COOKIES["device"]).exists():
                my_filter=Filters.objects.get(device=request.COOKIES["device"])
                for i in Filters.objects.filter(device=request.COOKIES["device"]):
              
                    i.processor.set(request.POST.get("processor"))
                    i.save()   
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
    static=Product.objects.all()[0:2]
    # for i in static:
    #     i.const=True
    #     i.save()
    if request.user.is_authenticated:
        if Filters.objects.filter(customer_id=request.user.id).exists():
            filter=Filters.objects.get(customer_id=request.user.id)
            my_order,ordered=Order.objects.get_or_create(customer_id=request.user.id,ordered=True,delivered=False)
            if filter.type.name == "Normal":
                product=Product.objects.filter(type=filter.type)     
            else:        
                # for i in filter.processor.all():                                            
                #     proc=i.name  
                product=Product.objects.filter(category=filter.category,processor__in=filter.processor.all()).distinct().order_by("-date_modified","id")
            paginator = Paginator(product,4) # Show 6 contacts per page.      

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
            my_order,created=Order.objects.get_or_create(device=request.COOKIES["device"],ordered=True,delivered=False)
 
            if my_filter.type.name == "Normal":  
                product=Product.objects.filter(type=my_filter.type)   
            else:  
                product=Product.objects.filter(category=my_filter.category,processor__in=my_filter.processor.all()).distinct().order_by("-date_modified","id")
            paginator = Paginator(product,4) # Show 25 contacts per page.

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)        
        else:
            messages.error(request,"you dont have order yet")
            return redirect(reverse("home:home"))   
    form=OrderForm(request.POST or None)
    if form.is_valid():  
        instance=form.save(commit=False)   
        if request.user.is_authenticated: 
            if Filters.objects.filter(customer_id=request.user.id).exists():
                customer=Customer.objects.get(name=request.user)
                order=Order.objects.filter(customer=customer,ordered=True,delivered=False)
                if order.exists():
                    my_order=Order.objects.get(customer=customer,ordered=True,delivered=False)
                    b=request.POST.getlist("products")
                    for i in order: 
                        i.products.add(request.POST.get("products")) 
                        i.save()    
                        # for d in b:
                        #     i.products.add(d)
                        #     i.save()
                           
                    # return redirect(reverse("home:result"))
                else:
                    Order.objects.create(customer=customer,ordered=True,delivered=False)
                    for i in order:   
                        i.products.set(form.cleaned_data.get("products"))
                        i.save()
                    # return redirect(reverse("home:result")) 
            else: 
                messages.error(request,"you dont have order yet")
                return redirect(reverse("home:home"))
                
            
        else:
            if Filters.objects.filter(device=request.COOKIES["device"]).exists():
                # my_customer=Customer.objects.get(device=request.COOKIES["device"])
                order=Order.objects.filter(device=request.COOKIES["device"],ordered=True,delivered=False)
                if order.exists():
                    # print(form.cleaned_data.get("products"))
                    b=request.POST.getlist("products")
                    for i in order:  
                        i.products.add(request.POST.get("products")) 
                        i.save() 
                                      
                    # return redirect(reverse("home:result"))
                else:    
                    Order.objects.create(device=request.COOKIES['device'],ordered=True,delivered=False)
                    for i in order:
                        i.products.set(form.cleaned_data.get("products"))
                        i.save()
                    # return redirect(reverse("home:result"))
                  
            else:
                messages.error(request,"you dont have order yet")
                return redirect(reverse("hme:home"))
    context={"products":page_obj,"orders":my_order,"static":static}   
    return render(request,"products.html",context)
      
def order_edit(request,slug):
    if request.user.is_authenticated:
        order=Order.objects.filter(customer_id=request.user.id,ordered=True,delivered=False)
        print(order)
        product=Product.objects.get(slug=slug)
        for i in order:   
            i.products.remove(product)      
    else:
        order=Order.objects.filter(device=request.COOKIES["device"],ordered=True,delivered=False)
        print(order)
        product=Product.objects.get(slug=slug)
        for i in order:   
            i.products.remove(product)  
    return redirect(reverse("home:result"))
  
def result(request):  
    gammes=Games.objects.all() 

    supplier=Supplier.objects.all()
    error=False
    if request.user.is_authenticated:
        order=Order.objects.filter(customer_id=request.user.id,ordered=True,delivered=False)
        filter=Filters.objects.filter(customer_id=request.user.id) 
        if filter.exists():
            my_filter=Filters.objects.get(customer_id=request.user.id)
            similar=Product.objects.filter(category=my_filter.category)[0:3]  | Product.objects.filter(processor__in=my_filter.processor.all()).distinct()[0:3]  | Product.objects.filter(type=my_filter.type)[0:3] 
            eng=Fps_Numbers.objects.filter(name__icontains="Engineer",category=my_filter.category)
            prog=Fps_Numbers.objects.filter(name__icontains="Programmer",category=my_filter.category)
        else:     
            messages.error(request,"you don't have order yet")
            return redirect(reverse("home:home")) 
        if order.exists():    
            my_order=Order.objects.get(customer_id=request.user.id,ordered=True,delivered=False)      
            if my_order.products.count() < 1:
                error=True                       
            for i in my_order.products.all():
                if my_order.products.filter(name__icontains="hard").exists() and my_order.products.filter(name__icontains="gpu").exists() and my_order.products.filter(name__icontains="motherboard").exists() and my_order.products.filter(name__icontains="ram").exists() and my_order.products.filter(name__icontains="processor") and my_order.products.filter(name__icontains="cooler") and my_order.products.filter(name__icontains="power supply").exists() :
                    error=False   
                elif my_order.products.filter(type__name="Normal").exists():
                    error=True
                    similar= Product.objects.filter(type=my_filter.type)[0:3] |Product.objects.filter(category=my_filter.category)[0:3] 

                else:       
                    error=True          
                    # messages.error(request,"make sure you have full package Gpu,Cpu,Ram,Motherboard and SSD")   
        
        else:
            messages.error(request,"you don't have order yet")
            return redirect(reverse("home:home"))            

        if request.method == "POST":  
            supplier=Supplier.objects.all()
            edit_filter=Filters.objects.get(customer_id=request.user.id)
            edit_filter.type, edit_filter.category = None,None
            edit_filter.processor.clear()
            edit_filter.save()     
            
            
            context={"user":request.user,"orders":Order.objects.get(customer_id=request.user.id,ordered=True,delivered=False),"suppliers":supplier}
            msg_html = render_to_string("message.html",context)
            msg = EmailMessage(subject="payment completed", body=msg_html, from_email=settings.EMAIL_HOST_USER, bcc=[request.user.email])
            msg.content_subtype = "html"  # Main content is now text/html
            msg.send()
            my_order.delivered=True
            my_order.save()     
            return redirect(reverse("home:confirm"))

 
      
    else:       
        order=Order.objects.filter(device=request.COOKIES["device"],ordered=True,delivered=False)
        filter=Filters.objects.filter(device=request.COOKIES["device"])
        if filter.exists():
            my_filter=Filters.objects.get(device=request.COOKIES["device"])
            eng=Fps_Numbers.objects.filter(name__icontains="Engineer",category=my_filter.category)
            prog=Fps_Numbers.objects.filter(name__icontains="Programmer",category=my_filter.category)
        if order.exists():
            my_order=Order.objects.get(device=request.COOKIES["device"],ordered=True,delivered=False)
            similar=Product.objects.filter(category=my_filter.category)[0:3]  | Product.objects.filter(processor__in=my_filter.processor.all()).distinct()[0:3]  | Product.objects.filter(type=my_filter.type)[0:3] 

            if my_order.products.count() < 1:
                error=True                       
            for i in my_order.products.all():
                if my_order.products.filter(name__icontains="ssd").exists() and my_order.products.filter(name__icontains="gpu").exists() and my_order.products.filter(name__icontains="motherboard").exists() and my_order.products.filter(name__icontains="ram").exists() and my_order.products.filter(name__icontains="cpu").exists() :
                    error=False   
                elif my_order.products.filter(type__name="Normal").exists():
                    error=True
                    similar= Product.objects.filter(type=my_filter.type)[0:3] |Product.objects.filter(category=my_filter.category)[0:3] 

                else:       
                    error=True 
        else:      
            messages.error(request,"you don't have order yet")
            return redirect(reverse("home:home"))  

    context={"prog":prog,"eng":eng,"orders":my_order,"similar":similar,"filters":my_filter,"suppliers":supplier,"gammes":gammes,"error":error} 
    return render(request,"result.html",context)  
 
def add_similar_product(request,id):
    product=Product.objects.get(id=id)
    if request.user.is_authenticated:
        order=Order.objects.get(customer_id=request.user.id,ordered=True,delivered=False)
        order.products.add(product)
        order.save()
        messages.success(request,"Product added Successfully")
    else:
        order=Order.objects.get(device=request.COOKIES["device"],ordered=True,delivered=False)
        order.products.add(product)
        order.save()
        messages.success(request,"Product added Successfully")

    return redirect(reverse("home:result"))
        
def remove_similar_product(request,id):
    product=Product.objects.get(id=id)
    if request.user.is_authenticated:
        order=Order.objects.get(customer_id=request.user.id,ordered=True,delivered=False)
        order.products.remove(product)
        messages.error(request,"Product removed Successfully")
    else:
        order=Order.objects.get(device=request.COOKIES["device"],ordered=True,delivered=False)
        order.products.remove(product)
        messages.error(request,"Product removed Successfully")

    return redirect(reverse("home:result"))

def confirm(request):
    if not request.user.is_authenticated:
        return redirect(reverse("home:home"))
    supplier=Supplier.objects.all()
    context={"supplier":supplier}
    return render(request,"confirm.html",context)   
                  
@login_required
def dashboard(request):  
    products=Product.objects.all().order_by("category")
    if not request.user.is_superuser:
        messages.error(request,"you dont have permission to add products")
        return redirect(reverse("home:home"))
    context={"products":products}
    return render(request,"dashboard/index.html",context)

def add(request):
    if not request.user.is_superuser:
        messages.error(request,"you dont have permission to add products")
        return redirect(reverse("home:home"))
    form =DashboardForm(request.POST or None ,request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request,"Product added successfully")
        return redirect(reverse("home:dashboard"))
    context={"form":form}
    return render(request,"dashboard/add.html",context)
       
def edit(request,slug):
    if not request.user.is_superuser:
        messages.error(request,"you dont have permission to add products")
        return redirect(reverse("home:home"))
    product=get_object_or_404(Product,slug=slug)
    form =DashboardForm(request.POST or None ,request.FILES or None,instance=product)
    if form.is_valid():
        form.save()
        messages.success(request,"Product updated successfully")
        return redirect(reverse("home:dashboard"))
    context={"form":form,"product":product}
    return render(request,"dashboard/edit.html",context)
       
def delete(request,slug):
    if not request.user.is_superuser:
        messages.error(request,"you dont have permission to add products")
        return redirect(reverse("home:home"))
    product=get_object_or_404(Product,slug=slug)
    
    product.delete()
    messages.success(request,"product deleted successfully")
    return redirect(reverse("home:dashboard"))   
    # return render(request,"dashboard/index.html")   
@login_required
def profile(request):
    order=Order.objects.filter(customer_id=request.user.id,ordered=True,delivered=True)
    context={"order":order}
    return render(request,"dashboard/profile.html",context)  
    # return render(request,"dashboard/index.html")   
def gammes(request):
    if not request.user.is_superuser:
        messages.error(request,"you dont have permission to add products")
        return redirect(reverse("home:home"))
    gammes=Games.objects.all()

    context={"gammes":gammes}
   
    return render(request,"dashboard/gammes.html",context)   


def fps(request):
    if not request.user.is_superuser:
        messages.error(request,"you dont have permission to add products")
        return redirect(reverse("home:home"))
    fps=Fps_Numbers.objects.all().order_by("name")

    context={"fps":fps}
   
    return render(request,"dashboard/fps.html",context) 
  
def fps_add(request):
    if not request.user.is_superuser:
        messages.error(request,"you dont have permission to add products")
        return redirect(reverse("home:home"))
    form=FpsForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request,"Fps Added successfully")
        return redirect(reverse("home:fps"))
    context={"form":form}
   
    return render(request,"dashboard/gammes_edit.html",context) 

def fps_edit(request,id):
    if not request.user.is_superuser:
        messages.error(request,"you dont have permission to add products")
        return redirect(reverse("home:home"))
    fps=Fps_Numbers.objects.get(id=id)
    form=FpsForm(request.POST or None,instance=fps)
    if form.is_valid():
        form.save()
        messages.success(request,"Fps changed successfully")
        return redirect(reverse("home:fps"))
    context={"form":form}
   
    return render(request,"dashboard/gammes_edit.html",context)   


def supplier(request):
    if not request.user.is_superuser:
        messages.error(request,"you dont have permission to add products")
        return redirect(reverse("home:home"))
    supplier=Supplier.objects.all()

    context={"supplier":supplier}
   
    return render(request,"dashboard/all-supplier.html",context)   
    
def add_supplier(request):
    if not request.user.is_superuser:
        messages.error(request,"you dont have permission to add products")
        return redirect(reverse("home:home"))
    form=SupplierForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request,"you added supplier")
        return redirect(reverse("home:suppliers"))
    context={"form":form}
   
    return render(request,"dashboard/add-supplier.html",context)   

def edit_supplier(request,id):
    if not request.user.is_superuser:
        messages.error(request,"you dont have permission to add products")
        return redirect(reverse("home:home"))
    supplier=Supplier.objects.get(id=id)
    form =SupplierForm(request.POST or None,instance=supplier)
    if form.is_valid():
        form.save()
        messages.success(request,"supplier added successfully")
        return redirect(reverse("home:suppliers"))
    context={"supplier":supplier,"form":form}
   
    return render(request,"dashboard/edit-supplier.html",context)   
def gammes_edit(request,slug):
    if not request.user.is_superuser:
        messages.error(request,"you dont have permission to add products")
        return redirect(reverse("home:home"))
    gamme=Games.objects.get(name=slug)
    form=GammesForm(request.POST or None,instance=gamme)
    if form.is_valid():
        form.save()
        messages.success(request,"Gamme changed successfully")
        return redirect(reverse("home:gammes"))
    context={"form":form}
   
    return render(request,"dashboard/gammes_edit.html",context)   

def team(request):      

    return render(request,"team.html")   

          