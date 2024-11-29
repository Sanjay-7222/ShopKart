from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib import messages
from django.http import HttpResponse
from .forms import *
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
import json
from django.db.models import Q
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    # q = request.GET.get('q') if request.GET.get('q') !=None else ""
    # prods = Product.objects.filter(
    #     Q(category__name__iconatains = q) |
    #     Q(name__iconatains = q) |
    #     Q(description__iconatains = q) 
    # )[0:2]
    products = Product.objects.filter(trending = 1)
    return render(request, 'index.html',{'products':products})

def add_to_cart(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.load(request)
            product_qty = data['product_qty']
            product_id = data['pid']
            # print(request.user.id) 
            product_status = Product.objects.get(id = product_id)
            if product_status:
                if Cart.objects.filter(user = request.user.id, product_id = product_id):
                    return JsonResponse({'status':'Product Already in Cart'}, status = 200)
                else:
                    if product_status.quantity >= product_qty:
                        Cart.objects.create(user = request.user, product_id = product_id, product_qty = product_qty)
                        return JsonResponse({'status':'Product Added to Cart'}, status = 200)
                    else:
                        return JsonResponse({'status': 'Product Stock not Available'}, status = 200)
        else:
            return JsonResponse({'status':'Login to Add Cart'},status = 200)
    else:
        return JsonResponse({'status':'Invalid Access'}, status = 200)
    
def fav_page(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.load(request)
            product_id = data['pid']
            product_status = Product.objects.get(id = product_id)
            if product_status:
                if Favourite.objects.filter(user = request.user.id, product_id = product_id):
                    return JsonResponse({'status': 'Product Already in Favourite'}, status = 200)
                else:
                    Favourite.objects.create(user = request.user, product_id = product_id)
                    return JsonResponse({'status': 'Product Added to Favourite'}, status = 200)
        else:
            return JsonResponse({'status': 'Login to Add Favourite'}, status = 200)
    else:
        return JsonResponse({'status': 'Invalid Access'}, status =200)
    
def fav_view(request):
    if request.user.is_authenticated:
        fav = Favourite.objects.filter(user = request.user)
        return render(request,'fav.html',{'fav':fav})
    else:
        return redirect('home')
    
def cart_page(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user = request.user)
        return render(request,'cart.html',{'cart':cart})
    else:
        return redirect('home')
    
def remove_fav(request,fid):
    item = Favourite.objects.get(id = fid)
    item.delete()
    return redirect('favview') 

def remove_cart(request,cid):
    cartitem = Cart.objects.get(id = cid)
    cartitem.delete()
    return redirect('cart') 
    
def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            name = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request,username = name, password = password)
            if user is not None:
                login(request,user)
                messages.success(request,"Logged in Successfully")
                return redirect('home')
            else:
                messages.error(request,"Invalid Username or Password")
                return redirect("login")
        return render(request,'login.html')

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged out Successfully")
    return redirect("home")

def register(request):
    form = CustomUserForm()
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            form.save()
            login(request,user)
            messages.success(request,"Registration Success You can Login Now..!")
            return redirect('home')
    return render(request, 'register.html',{'form': form})
 
def collection(request):
    category = Category.objects.filter(status = 0)
    return render(request, 'collection.html', {'category': category})

def collectionview(request,name):
    if (Category.objects.filter(status = 0, name = name)):
        products = Product.objects.filter(category__name = name)
        return render(request, 'product.html', {'products': products, 'category_name':name})
    
    else:
        messages.warning(request,"No Such Category Found")
        return redirect('collection')
    
def product_details(request,cname,pname):
    if (Category.objects.filter(status = 0, name = cname)):
        if (Product.objects.filter(status = 0, name = pname)):
            products = Product.objects.filter(name = pname, status = 0).first()
            return render(request, 'product_detail.html', {'products': products})
        
        else:
            messages.error(request, "No Such Product Found")
            return redirect('collection')
    
    else:
        messages.error(request,"No Such Category Found")
        return redirect('collection')
    
def checkout(request):
    form = CheckoutForm()
    user_cart = Cart.objects.filter(user=request.user)
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            total_cost = sum(cart_item.total_cost for cart_item in user_cart)
            checkout_instance = form.save(commit=False)
            checkout_instance.user = request.user
            checkout_instance.total_cost = total_cost
            
            # Save the checkout instance to the database
            checkout_instance.save()
            
            # Delete the items from the user's cart after successful checkout
            user_cart.delete()
            
            messages.success(request, "Your Products will be delivered in 2-5 working days")
            return redirect('cart')  # Redirect to the cart page or another page as needed
        else:
            messages.error(request, "There was an error in your form. Please correct it.")
    return render(request, 'cart.html', {'form': form, 'user_cart': user_cart})