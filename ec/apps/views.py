from urllib import request
from django.http import HttpResponse, JsonResponse
from django.db.models import Count
from django.shortcuts import render, redirect
from django.views import View
from .models import Product, Customer, Cart, OrderPlaced, Wishlist
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@login_required
# Create your views here.
def home(request):
    wishitem = 0
    if request.user.is_authenticated:
        wishitem = Wishlist.objects.filter(user=request.user).count()
    return render(request, 'home.html', {'wishitem': wishitem})

@login_required
def about(request):
    wishitem = 0
    if request.user.is_authenticated:
        wishitem = Wishlist.objects.filter(user=request.user).count()
    return render(request, 'about.html', locals())

@login_required
def contact(request):
    wishitem = 0
    if request.user.is_authenticated:
        wishitem = Wishlist.objects.filter(user=request.user).count()
    return render(request, 'contact.html', {'wishitem': wishitem})

@method_decorator(login_required, name = 'dispatch')
class CategoryView(View):
    def get(self,request,val):
        product = Product.objects.filter(category = val)
        title = Product.objects.filter(category = val).values('title').annotate(total = Count('title'))
        return render(request, "category.html",locals())
    
@method_decorator(login_required, name = 'dispatch')
class CategoryTitle(View):
    def get(self,request,val):
        product = Product.objects.filter(title = val)
        title = Product.objects.filter(category = product[0].category).values('title')
        return render(request, "category.html",locals())
    
@method_decorator(login_required, name = 'dispatch')
class ProductDetail(View):
    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            if request.user.is_authenticated:
                wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user))
            else:
                wishlist = None  # Handle case where user is not authenticated
            return render(request, "productdetail.html", {'product': product, 'wishlist': wishlist})
        except Product.DoesNotExist:
            # Handle case where product with given pk does not exist
            return render(request, "product_not_found.html")
    
class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, "registration.html",locals())
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! User Registration Successfully Completed")
        else:
            messages.warning(request, "Invalid Data Inputed")
        return render(request, "registration.html", locals())

class LoginView(View):
    def get(self, request):
        return render(request, "login.html",locals())
    
@method_decorator(login_required, name = 'dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, "profile.html", locals())

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']  # Corrected field name
            city = form.cleaned_data['city']
            phone_no = form.cleaned_data['phone_no']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            # Corrected field name 'loacality' to 'locality'
            reg = Customer(user=user, name=name, locality=locality, phone_no=phone_no, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, "Congratulations! User Registration Successfully Completed")
        else:
            messages.warning(request, "Invalid Data Inputed")

        return render(request, "profile.html", locals())
    
@login_required
def address(request):
     add = Customer.objects.filter(user=request.user)
     return render(request, "address.html", locals())

@method_decorator(login_required, name = 'dispatch')
class updateAddress(View):
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, "updateAddress.html", locals())
    def post(self, request, pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.phone_no = form.cleaned_data['phone_no']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request, "Congratulations! Profile Update Successfully")
        else:
            messages.warning(request, "Invalid Data Inputed")
        return redirect("address")

@login_required    
def add_to_cart(request):
    user=request.user
    if request.method == "GET":
        product_id=request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect("/cart")

@login_required
def show_cart (request):
    user = request.user  
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value 
    totalamount = amount + 40
    return render(request, 'addtocart.html',locals())

@method_decorator(login_required, name = 'dispatch')
class checkout(View):
    def get(self, request):
        user= request.user
        add = Customer.objects.filter(user=user)
        cart_items= Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
        totalamount= famount + 40
        return render(request, 'checkout.html', locals())
    
@login_required
def payment_done(request):
    user= request.user
    cart = Cart.objects.filter(user = user)
    for c in cart:
        OrderPlaced(user= user, customer= user.customer, product=c.product, quantity= c.quantity, payment= c.payment).save()
        c.delete()
    return redirect("orders")
    
@login_required
def orders(request):
    order_placed = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'orders.html', locals())


@login_required
def plus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        #print(prod_id)
        data={
             'quantity': c.quantity,
             'amount': amount,
             'totalamount' : totalamount
        }
        return JsonResponse(data)
    
@login_required
def minus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        #print(prod_id)
        data={
             'quantity': c.quantity,
             'amount': amount,
             'totalamount' : totalamount
        }
        return JsonResponse(data)
    
@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        #print(prod_id)
        data={
             'amount': amount,
             'totalamount' : totalamount
        }
        return JsonResponse(data)

def plus_wishlist(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        product = Product.objects.get(id = prod_id)
        user = request.user
        Wishlist(user = user , product = product). save()
        data = {
            'message' : 'Wishlist Added Successfully',
        }
        return JsonResponse(data)
    
def minus_wishlist(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        product = Product.objects.get(id = prod_id)
        user = request.user
        Wishlist.objects.filter(user = user , product = product). delete()
        data = {
            'message' : 'Wishlist Remove Successfully',
        }
        return JsonResponse(data)
    
@login_required
def search(request):
    query = request.GET.get('search')
    products = Product.objects.filter(title__icontains=query) if query else None
    return render(request, 'search_results.html', {'products': products, 'query': query})