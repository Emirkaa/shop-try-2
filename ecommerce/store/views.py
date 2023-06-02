from django.db.models import Count
from django.http import  JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.shortcuts import render
from .models import *
from .forms import *
from django.contrib import messages
from .models import Customer
from django.db.models import Q
import razorpay
from django.conf import settings


def home_page(request):
    x = 0
    w = 0
    if request.user.is_authenticated:
        w = len(WishList.objects.filter(user=request.user))
        x = len(Cart.objects.filter(user=request.user))
    return render(request, 'store/home.html', locals())

def contact(request):
    x = 0
    w = 0
    if request.user.is_authenticated:
        w = len(WishList.objects.filter(user=request.user))
        x = len(Cart.objects.filter(user=request.user))
    return render(request, 'store/contact.html', locals())

def about(request):
    x = 0
    w = 0
    if request.user.is_authenticated:
        w = len(WishList.objects.filter(user = request.user))
        x = len(Cart.objects.filter(user=request.user))
    return render(request,'store/about.html', locals())

class CategoryView(View):
    def get(self, request, val):
        
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        x = 0
        w = 0
        if request.user.is_authenticated:

            w = len(WishList.objects.filter(user = request.user))
            x = len(Cart.objects.filter(user=request.user))
        return render(request, 'store/category.html', locals())
    
class CategoryTitle(View):
    def get(self, request, val):
        
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title') 
        x = 0
        w = 0
        if request.user.is_authenticated:
            w = len(WishList.objects.filter(user = request.user))
            x = len(Cart.objects.filter(user=request.user))
        return render(request, 'store/category.html', locals())

class ProductDetail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        w = len(WishList.objects.filter(Q(product=product) & Q(user=request.user)))
        
        x = 0
        if request.user.is_authenticated:
            x = len(Cart.objects.filter(user=request.user))
        return render(request, 'store/productdetail.html', locals())
    
class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        x = 0
        w = 0
        if request.user.is_authenticated:
            w = len(WishList.objects.filter(user = request.user))
            x = len(Cart.objects.filter(user=request.user))
        return render(request, 'store/registration.html', locals())
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Поздравляем! Пользователь успешно зарегестрирован!')
        else:
            messages.warning(request, 'Ошибка. Проверьте введенные вами данные.')
        return render(request, 'store/registration.html', locals())
    

        
    
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        x = 0
        w = 0
        if request.user.is_authenticated:
            w = len(WishList.objects.filter(user = request.user))
            x = len(Cart.objects.filter(user=request.user))
        return render(request,'store/profile.html', locals())
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            country = form.cleaned_data['country']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(user=user, name=name, locality=locality, city=city, mobile=mobile, country=country, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Профиль успешно сохранен.')
        else:
            messages.warning(request,'Неверные входные данные.')
        return render(request,'store/profile.html',locals()) 
    

def address(request):
    add = Customer.objects.filter(user=request.user)
    x = 0
    w = 0
    if request.user.is_authenticated:
        w = len(WishList.objects.filter(user = request.user))
        x = len(Cart.objects.filter(user=request.user))
    return render(request, 'store/address.html', locals())

class UpdateAddress(View):
    def get(self,request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        x = 0
        w = 0
        if request.user.is_authenticated:
            w = len(WishList.objects.filter(user = request.user))
            x = len(Cart.objects.filter(user=request.user))
        return render(request, 'store/updateAddress.html', locals())
    def post(self, request, pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.country = form.cleaned_data['country']
            add.zipcode = form.cleaned_data['zipcode']
            
            add.save()
            messages.success(request, 'Профиль успешно отредактирован!')
        else:
            messages.warning(request, 'Ошибка! Проверьте введенные вами данные!')
        return redirect('address')
    

def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()

    return redirect('/cart')


def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    
    for p in cart:
        x = p.quantity * p.product.discounted_price
        x = x + amount
        totalamount = x + 40
    x = 0
    w = 0
    if request.user.is_authenticated:
        w = len(WishList.objects.filter(user = request.user))
        x = len(Cart.objects.filter(user=request.user))
    
    return render(request, 'store/addtocart.html', locals())



def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id)& Q(user=request.user))
        c.quantity += 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            v = p.quantity * p.product.discounted_price
            amount = amount + v
        totalamount = amount + 40
        data = {

            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id)&Q(user=request.user))
        c.quantity -= 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            v = p.quantity * p.product.discounted_price
            amount = amount + v
            if p.quantity == 0:
                c.delete()
                c.save()
        totalamount = amount + 40
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        
        return JsonResponse(data)
    
def remove_cart(request):
    if request.method == 'GET':
        
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id)&Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            v = p.quantity * p.product.discounted_price
            amount = amount + v
            x = 0
        totalamount = amount + 40
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        
        return JsonResponse(data)
    

    

def order_page(request):
    orders_placed = OrderPlaced.objects.filter(user=request.user)
    x = 0
    w = 0
    if request.user.is_authenticated:
        w = len(WishList.objects.filter(user = request.user))
        x = len(Cart.objects.filter(user=request.user))
    return render(request, 'store/orders.html', locals())

    
class checkout(View):
    def get(self,request):
        x = 0
        w = 0
        if request.user.is_authenticated:
            w = WishList.objects.filter(user = request.user)
            x = len(Cart.objects.filter(user=request.user))
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        f = 0
        for p in cart_items:
            v = p.quantity * p.product.discounted_price
            f = v + 40
        totalamount = f
        razoramount = int(totalamount * 100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))

        data = {'amount':razoramount, 'currency':'USD', 'receipt':'order_rcptid_11'}
        payment_responce = client.order.create(data=data)
        print(payment_responce)

        order_id = payment_responce['id']
        order_status = payment_responce['status']
        if order_status == 'created':
            payment = Payment(
                user=user,
                amount = totalamount,
                razorpay_order_id = order_id,
                razorpay_payment_status = order_status
            )
            payment.save()
        return render(request,'store/checkout.html', locals())

def payment_done(request):
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')
    user = request.user
    customer = Customer.objects.get(id=cust_id)

    payment = Payment.objects.get(razorpay_order_id=order_id)
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer, product=c.product, quantity = c.quantity, payment=payment).save()
        c.delete()
    return redirect('orders')


def plus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        WishList(user=user, product=product).save()
        data = {
            'message':'Добавлено в список желаемого!'
        }
        return JsonResponse(data)














        


