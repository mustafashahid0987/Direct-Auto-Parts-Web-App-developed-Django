from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse, request
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.contrib.auth.models import User
from collections import OrderedDict
from django.http import JsonResponse
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import View
from django.core.files import File
from .models import *
import time
import json
from datetime import datetime

def index(request):

    cat = Category.objects.all()
    subcat = Subcategory.objects.all()


    blog = blogs.objects.all()
    context = {
        'blogs':blog,
        'categories':cat,
        'subcat':subcat,
    }

    return render(request,'website/index.html',context)

def subcategory_view(request):
    if request.method == 'GET':
        category_id = request.GET.get('category_id')
        subcategory_id = request.GET.get('subcategory')
        if category_id and subcategory_id:
            category = Category.objects.get(id=category_id)
            subcategory = Subcategory.objects.get(id=subcategory_id)
            products = Product.objects.filter(subcategory=subcategory)
            if products.exists():
                context = {
                    'category': category,
                    'subcategory': subcategory,
                    'products': products
                }

                return render(request, 'website/product_list.html', context)
            
            else:
                messages.error(request, "Products for this subcategory will be uploaded soon.")

                return render(request, 'website/index.html')
        
    return redirect('index')


def subcategory_base(request, category_id, subcategory_id):
    if request.method == 'GET':
        category = get_object_or_404(Category, id=category_id)
        subcategory = get_object_or_404(Subcategory, id=subcategory_id)
        products = Product.objects.filter(subcategory=subcategory)
        
        if products.exists():
            context = {
                'category': category,
                'subcategory': subcategory,
                'products': products
            }

            return render(request, 'website/product_list.html', context)
        
        else:
            messages.error(request, "Products for this subcategory will be uploaded soon.")

            return render(request, 'website/index.html')
        
    else:
        return redirect('index')
    

def about(request):
    return render(request,'website/about.html')

def contact(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email =request.POST.get('email')
        subject =request.POST.get('subject')
        message =request.POST.get('message')
        contact_obj = contact_us.objects.create(first_name=first_name, last_name=last_name, email=email, subject=subject, message=message)
        messages.success(request, 'you query is received. we will reply you soon.')
        contact_obj.save()

        return redirect('index')
    
    return render(request,'website/contact.html')

@csrf_exempt
def checkout(request):

    print('checkout chala')

    if request.method == 'POST':
        selected_payment_method = request.POST.get('pay')


    if selected_payment_method == 'bank':
        payment_method = 'bank'
        bd_obj = Bank_details.objects.all()
        bd_obj = bd_obj[0]

    elif selected_payment_method == 'crypto':
        payment_method = 'crypto'
        bd_obj = crypto.objects.all()
        bd_obj = bd_obj[0]


    ob = addtocart.objects.filter(user_id=request.user.id)

    # print(ob)

    lst=[]
    quantity_lst = []
    subtotal_lst = []
    cart_id_lst = []
    subtotal = 0

    for o in range(len(ob)):
        lst1=[]
        quantity_lst.append(ob[o].quantity)
        cart_id_lst.append(ob[o].id)
        # print("ss", ob[o].id)

        for i in ob[o].coin_ids.all():
            obj1 = Product.objects.get(id=i.id)
            # print("mustafa",float(obj1.price))
            subtotal += float(ob[o].quantity * obj1.price)

            subtotal_lst.append(ob[o].quantity * obj1.price)
            lst1.append(obj1)
            lst.append(lst1)

            # for product in obj1:
            #     subtotal += product.price_per_pack

            

    all_data = zip(quantity_lst,lst,subtotal_lst, cart_id_lst)
    # context = {'all_data':all_data,'subtotal':subtotal, 'discount_instance':discount_instance}
    context = {
        'all_data':all_data,
        'subtotal':subtotal,
        'payment_method':payment_method,
        'bank_obj':bd_obj,
        }

    return render(request,'website/checkout.html',context)

def product_list(request):
    return render(request,'website/product_list.html')

def product_detail(request, pk):

    product_data = Product.objects.filter(id=int(pk))
    context = {'product_data':product_data}
    # print(product_data) 

    return render(request,'website/product_detail.html', context)

def login_page(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password =request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            print("USER",user)
            if user is not None:
                login(request, user)
                print("LOGGED IN")
                # logout(request)
                messages.success(request, 'you are login sucessfully')
                return redirect('index')
            else:
                print('else chala')
                messages.error(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'website/login.html', context)

def logoutP(request):
    logout(request)
    return redirect('login')


def register(request):
    if request.method == 'POST':
        # Retrieve form data from POST request
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        company_name = request.POST.get('company_name')
        street_address_1 = request.POST.get('street_address_1')
        street_address_2 = request.POST.get('street_address_2')
        zip_code = request.POST.get('zip_code')
        city = request.POST.get('city')
        country = request.POST.get('country')
        state = request.POST.get('state')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if the passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('register')  # Redirect to registration page with error message
        
        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')  # Redirect to registration page with error message

        # Check if the email is already registered
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('register')  # Redirect to registration page with error message

        # Create a new user object
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )

        # Create a UserProfile instance and associate it with the newly created user
        user_profile = UserProfile.objects.create(
            user=user,
            company_name=company_name,
            street_address_1=street_address_1,
            street_address_2=street_address_2,
            zip_code=zip_code,
            city=city,
            country=country,
            state=state,
            phone=phone
        )

        messages.success(request, "Registration successful. Please log in.")
        return redirect('login')  # Redirect to login page with success message

    return render(request, 'website/register.html')  # Render registration form template

@login_required(login_url='login')
def newsletter_sub(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        # Check if the email already exists in the database
        if newsletter.objects.filter(email=email).exists():
            messages.error(request, 'You are already subscribed.')
            return redirect('index')

        # If the email does not exist, save it
        newsletter_obj = newsletter.objects.create(email=email)
        messages.success(request, 'You have successfully subscribed.')
        newsletter_obj.save()
        return redirect('index')

    return redirect('index')  # If request method is not POST, redirect to index page


def blog_detail(request,pk):
    # user_name = request.user.first_name
    blog_details = blogs.objects.filter(id=int(pk))

    for b in blog_details:
        title = b.title

    context = {'blog_details':blog_details, 'title':title}
    # print(product_data) 
    return render(request, 'website/blog_detail.html', context)


def add_to_cart(request,pk):

    user_id = request.user.id
    # print(pk)
    cc=Product.objects.get(id=pk)
    print("coin",cc)
    data=addtocart.objects.filter(Q(user_id=user_id) & Q(coin_ids__id=pk))
    if not data:
        print("No data")
        obj=addtocart.objects.create(user_id=user_id, quantity= 1)
        obj.save()
        obj.coin_ids.add(cc)
        messages.success(request, 'Product is sucessfully added to your cart..')
        return redirect('cart')
    else:
        print("already")

    return render(request,'website/cart.html')

def remove_cart(request,pk):
    print('main hoon',pk, request.user.id)
    obj=addtocart.objects.get(coin_ids=pk, user_id=request.user.id)
    obj.delete()
    print("muti",pk)
    print(obj)
    #return render(request,"coin/watchlist.html")
    return redirect("cart")

def cart(request):

    #code of get data of discount coupon start here..
    # try:
    #     # Retrieve the user based on the user_id
    #     user = User.objects.get(id=request.user.id)
    #     print(user)
    #     # Retrieve the discount_table instance for the user
    #     discount_instance = discount_table.objects.get(user_ids=user)
    #     # print('disount coupon',discount_instance)

    # except:
    #     discount_instance = 'none'
    #     print('you does not have the discount coupon')
    #code of get data of discount coupon ends here...



    ob = addtocart.objects.filter(user_id=request.user.id)

    # print(ob)

    lst=[]
    quantity_lst = []
    subtotal_lst = []
    cart_id_lst = []
    subtotal = 0

    for o in range(len(ob)):
        lst1=[]
        quantity_lst.append(ob[o].quantity)
        cart_id_lst.append(ob[o].id)
        # print("ss", ob[o].id)

        for i in ob[o].coin_ids.all():
            obj1 = Product.objects.get(id=i.id)
            # print("mustafa",float(obj1.price))
            subtotal += float(ob[o].quantity * obj1.price)

            subtotal_lst.append(ob[o].quantity * obj1.price)
            lst1.append(obj1)
            lst.append(lst1)

            # for product in obj1:
            #     subtotal += product.price_per_pack

            

    all_data = zip(quantity_lst,lst,subtotal_lst, cart_id_lst)
    # context = {'all_data':all_data,'subtotal':subtotal, 'discount_instance':discount_instance}
    context = {'all_data':all_data,'subtotal':subtotal}
    return render(request,'website/cart.html', context)

def add_to_watchlist(request,pk):

    user_id = request.user.id
    # print(pk)
    cc=Product.objects.get(id=pk)
    print("coin",cc)
    data=watchlist.objects.filter(Q(user_id=user_id) & Q(coin_ids__id=pk))
    if not data:
        print("No data")
        obj = watchlist.objects.create(user_id=user_id)
        obj.save()
        obj.coin_ids.add(cc)
        messages.success(request, 'Product is sucessfully added to your wishlist..')
        return redirect('watchlist')
    else:
        print("already")

    return render(request,"website/wishlist.html")

def remove_watchlist(request,pk):
    print('main hoon',pk, request.user.id)
    obj=watchlist.objects.get(coin_ids=pk, user_id=request.user.id)
    obj.delete()
    print("muti",pk)
    print(obj)
    #return render(request,"coin/watchlist.html")
    return redirect("watchlist")

def wishlist(request):
    ob = watchlist.objects.filter(user_id=request.user.id)
    print(ob)

    lst=[]
    sign_no = []

    for o in range(len(ob)):
        lst1=[]
        print("ss",ob[0].coin_ids.all())
        sign_no.append(o+1)
        for i in ob[o].coin_ids.all():
            obj1 = Product.objects.get(id=i.id)
            # print("mustafa",obj1)
            lst1.append(obj1)
            lst.append(lst1)

    all_data = zip(sign_no,lst)
    context = {'all_data':all_data}
    return render(request,'website/wishlist.html', context)


def search_products(request):
    if request.method == 'GET':
        query = request.GET.get('q', '')  # 'q' is the name of the search input field
        if query:
            products = Product.objects.filter(name__icontains=query)
        else:
            products = Product.objects.all()  # Or any default queryset if no search query
        context = {'products': products, 'query': query}
        return render(request, 'website/product_list.html', context)
    

def blog(request):
    
    blog = blogs.objects.all()

    print(blog)
    context = {
        'blogs':blog,
    }

    return render(request,'website/blog.html', context)




def add_quantity(request, pk):
    user_id = request.user.id
    # Retrieve the instance of addtocart
    item = addtocart.objects.filter(user_id=user_id, coin_ids__id=pk).first()

    # If the item exists, increase its quantity by one
    if item:
        item.quantity += 1
        item.save()

    return redirect('cart')


def reduce_quantity(request, pk):
    user_id = request.user.id
    # Retrieve the instance of addtocart
    item = addtocart.objects.filter(user_id=user_id, coin_ids__id=pk).first()

    # If the item exists and its quantity is greater than 1, reduce its quantity by one
    if item and item.quantity > 1:
        item.quantity -= 1
        item.save()

    return redirect('cart')


@login_required(login_url='login')
def add_order(request):

    ob = addtocart.objects.filter(user_id=request.user.id)

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_no = request.POST.get('phone_no')
        email = request.POST.get('email')
        country = request.POST.get('country')
        address = request.POST.get('address')
        postal_code = request.POST.get('postal_code')
        payment_proof = request.FILES['pf_image']
        order_price = request.POST.get('order_price')

        discount_obj = request.POST.get('discount_obj')
        print(discount_obj)


        user_id = request.user.id
        print('add order',payment_proof)


        obj=order.objects.create(user_id=user_id,
                                 first_name = first_name,
                                 last_name = last_name,
                                country=country,
                                address=address,
                                phone_no=phone_no,
                                email=email,
                                postal_code = postal_code,
                                payment_proof=payment_proof,
                                price = order_price,
                                status='Unpaid',
                                fulfilment_status='Unfulfilled')
        obj.save()

        

        for o in range(len(ob)):
            print("add order...",ob[0].coin_ids.all())

            for i in ob[o].coin_ids.all():
                obj1 = Product.objects.get(id=i.id)
                obj.coin_ids.add(obj1)


        messages.success(request, 'Your payment is under review..')
        ob.delete()
        
        # dis_obj = discount_table.objects.get(id=discount_obj)
        # dis_obj.order_limit -= 1
        # dis_obj.save()

        # return redirect("my_order")
    
    return redirect('cart')


def user_dashboard(request):
    ob = order.objects.filter(user_id=request.user.id)

    order_obj = order.objects.all()
    total_orders = order.objects.count()
    total_sales = 0
    total_users = User.objects.count()
    total_products = Product.objects.count()

    for ord in order_obj:
        total_sales += ord.price


    print('my order',ob)

    context = {
                'orders':ob,
                'total_orders':total_orders,
                'total_sales':total_sales,
                'total_users':total_users,
                'total_products':total_products,
               }
    
    return render(request,'website/user_dashboard.html',context)


def all_blogs(request):

    product_obj = blogs.objects.all()

    context = {
        'products':product_obj,
    }

    return render(request,'website/all_blogs.html',context)


def all_contact(request):

    product_obj = contact_us.objects.all()

    context = {
        'products':product_obj,
    }

    return render(request,'website/all_contact.html',context)

def all_newsletters(request):

    product_obj = newsletter.objects.all()

    context = {
        'products':product_obj,
    }

    return render(request,'website/all_newsletters.html',context)

def all_products(request):

    product_obj = Product.objects.all()

    context = {
        'products':product_obj,
    }

    return render(request,'website/all_products.html',context)

def all_users(request):

    product_obj = UserProfile.objects.all()

    context = {
        'products':product_obj,
    }

    return render(request,'website/all_users.html',context)

def add_product(request):

    if request.method == "POST":
        submission_date = datetime.now()
        subcategory_id = request.POST.get('subcategory')
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')

        subcategory = Subcategory.objects.get(id=subcategory_id)
        product = Product.objects.create(submission_date=submission_date, subcategory=subcategory, name=name, desc=desc, price=float(price.replace(',', '')), quantity=quantity)

        # Handling product images (assuming multiple images can be uploaded)
        for image_file in request.FILES.getlist('images'):
            ProductImage.objects.create(product=product, image_file=image_file)

        messages.success(request, 'Product is succesfully added..')


        return redirect('product_list') 
    

    sub_obj = Subcategory.objects.all()

    context = {
        'subcategories':sub_obj,
    }

    return render(request,'website/add_product.html',context)


def promotion_details(request):
    return render(request,'website/promotion_details.html')

def shipping_information(request):
    return render(request,'website/shipping_information.html')

def service_department(request):
    return render(request,'website/service_department.html')

def customer_service(request):
    return render(request,'website/customer_service.html')

def ordering(request):
    return render(request,'website/ordering.html')

def exporting(request):
    return render(request,'website/exporting.html')

def returns(request):
    return render(request,'website/returns.html')

def core_return_policy(request):
    return render(request,'website/core_return_policy.html')

def return_material_request(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email =request.POST.get('email')
        subject =request.POST.get('subject')
        message =request.POST.get('message')
        contact_obj = contact_us.objects.create(first_name=first_name, last_name=last_name, email=email, subject=subject, message=message)
        messages.success(request, 'you request is received. we will reply you soon. Dont worry')
        contact_obj.save()

        return redirect('index')
    
    return render(request,'website/return_material_request.html')