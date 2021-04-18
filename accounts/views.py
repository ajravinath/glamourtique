from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from .models import *
from .forms import OrderForm, ProductForm, CustomerForm, CreateUserForm, AuthenticateUserForm
from .filters import OrderFilter
from .paginator import Paginator
from .decorators import unauthenticated_user, allowed_users


@login_required(login_url='login')
@allowed_users(allowed_roles=['admins'])
def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, f'Account was created for {username}')
            return redirect('login')

    else:
        form = CreateUserForm()

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@unauthenticated_user
def loginPage(request):
    form = AuthenticateUserForm(request.POST)
    if request.method == 'POST':
        form = AuthenticateUserForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(
                request, username=username, password=password)
            if user is not None:
                login(request, user)
                # messages.info(request, f"You are now logged in as {username}!")
                return redirect("home")
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid username or password')

    else:
        form = AuthenticateUserForm()

    context = {'form': form}
    return render(request, 'accounts/login.html', context)


def logout_request(request):
    logout(request)
    # messages.info(request, 'Logged out successfully!')
    return redirect('login')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admins'])
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    orderFilters = OrderFilter(request.GET, queryset=orders)
    orders = orderFilters.qs

    page_obj = Paginator(queryset=orders, request=request).get_page()

    context = {'orders': orders,
               'page': page_obj,
               'customers': customers,
               'total_orders': total_orders,
               'delivered': delivered,
               'pending': pending,
               'orderFilters': orderFilters
               }

    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admins'])
def products(request):
    products = Product.objects.all()

    page_obj = Paginator(queryset=products, request=request).get_page()

    context = {'products': products, 'page': page_obj}

    return render(request, 'accounts/products.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admins'])
def customersList(request):
    customers = Customer.objects.all()

    page_obj = Paginator(queryset=customers, request=request).get_page()

    context = {'customers': customers, 'page': page_obj}

    return render(request, 'accounts/customers_list.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admins'])
def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)
    customers = Customer.objects.all()
    customerOrders = customer.order_set.all()

    page_obj = Paginator(queryset=customerOrders, request=request).get_page()

    context = {'customers': customers, 'customer': customer, 'page': page_obj}

    return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admins'])
def createOrder(request):
    form = OrderForm()

    if request.method == 'POST':
        print('Printing form: ', request.POST)
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admins'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        print('Printing form: ', request.POST)
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admins'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {'item': order,  'redirectTo': 'home'}
    return render(request, 'accounts/delete.html', context)


# ---------

@login_required(login_url='login')
@allowed_users(allowed_roles=['admins'])
def createProduct(request):
    form = ProductForm()

    if request.method == 'POST':
        print('Printing form: ', request.POST)
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/products/')

    context = {'form': form}
    return render(request, 'accounts/product_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admins'])
def updateProduct(request, pk):
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)

    if request.method == 'POST':
        print('Printing form: ', request.POST)
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('/products/')
    # print('image', product.image.url, product)
    context = {'form': form, 'product': product}
    return render(request, 'accounts/product_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admins'])
def deleteProduct(request, pk):
    product = Product.objects.get(id=pk)

    if request.method == 'POST':
        product.delete()
        return redirect('/products/')

    context = {'item': product,  'redirectTo': 'products'}
    return render(request, 'accounts/delete.html', context)


# ---------


@login_required(login_url='login')
@allowed_users(allowed_roles=['admins'])
def createCustomer(request):
    form = CustomerForm()

    if request.method == 'POST':
        print('Printing form: ', request.POST)
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/customer_list/')

    context = {'form': form}
    return render(request, 'accounts/customer_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admins'])
def updateCustomer(request, pk):
    customer = Customer.objects.get(id=pk)
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        print('Printing form: ', request.POST)
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/customer_list/')

    context = {'form': form}
    return render(request, 'accounts/customer_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admins'])
def deleteCustomer(request, pk):
    customer = Customer.objects.get(id=pk)

    if request.method == 'POST':
        customer.delete()
        return redirect('/customer_list/')

    context = {'item': customer, 'redirectTo': 'customer_list'}
    return render(request, 'accounts/delete.html', context)
