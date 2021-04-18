from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logout_request, name="logout"),

    path('', views.home, name="home"),
    path('products/', views.products, name="products"),
    path('customer_list/', views.customersList, name="customer_list"),
    path('customer/<str:pk_test>/', views.customer, name="customer"),

    path('create_order/', views.createOrder, name="create_order"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),

    path('create_product/', views.createProduct, name="create_product"),
    path('update_product/<str:pk>/', views.updateProduct, name="update_product"),
    path('delete_product/<str:pk>/', views.deleteProduct, name="delete_product"),

    path('create_customer/', views.createCustomer, name="create_customer"),
    path('update_customer/<str:pk>/',
         views.updateCustomer, name="update_customer"),
    path('delete_customer/<str:pk>/',
         views.deleteCustomer, name="delete_customer"),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
         name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"),
         name="password_reset_confirm"),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(
        template_name="accounts/password_reset_complete.html"), name="password_reset_complete"),
]

urlpatterns += staticfiles_urlpatterns()
