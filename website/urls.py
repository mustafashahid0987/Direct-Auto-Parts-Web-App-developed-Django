from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns=[
    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('cart/',views.cart,name='cart'),
    path('blog/',views.blog,name='blog'),
    path('checkout/',views.checkout,name='checkout'),

    path('product_list/',views.product_list,name='product_list'),
    path('product_detail/<str:pk>/',views.product_detail,name='product_detail'),
    
    path('login/',views.login_page,name='login'),
    path('logout/',views.logoutP,name='logout'),
    path('register/',views.register,name='register'),
    path('newsletter_sub/',views.newsletter_sub,name='newsletter'),
    path('blog_detail/<str:pk>',views.blog_detail,name='blog_detail'),
    path('subcategory/', views.subcategory_view, name='subcategory_view'),

    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<str:pk>/', views.add_to_cart, name='add_to_cart'),
    path('remove_cart/<str:pk>/', views.remove_cart, name='remove_cart'), 

    path('add_to_watchlist/<str:pk>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('remove_watchlist/<str:pk>/', views.remove_watchlist, name='remove_watchlist'),
    path('watchlist/', views.wishlist, name='watchlist'),
    path('subcategory/<int:category_id>/<int:subcategory_id>/', views.subcategory_base, name='subcategory_base'),

    path('search/', views.search_products, name='search_products'),

    path('add_quantity/<str:pk>/', views.add_quantity, name='add_quantity'),
    path('reduce_quantity/<str:pk>/', views.reduce_quantity, name='reduce_quantity'),

    path('add_order/', views.add_order, name='add_order'),

    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),

    path('all_newsletters/', views.all_newsletters, name='all_newsletters'),
    path('all_contact/', views.all_contact, name='all_contact'),
    path('all_blogs/', views.all_blogs, name='all_blogs'),
    path('all_users/', views.all_users, name='all_users'),
    path('all_products/', views.all_products, name='all_products'),
    path('add_product/', views.add_product, name='add_product'),

    path('promotion_details/', views.promotion_details, name='promotion_details'),
    path('shipping_information/', views.shipping_information, name='shipping_information'),
    path('service_department/', views.service_department, name='service_department'),
    path('customer_service/', views.customer_service, name='customer_service'),
    path('ordering/', views.ordering, name='ordering'),
    path('exporting/', views.exporting, name='exporting'),
    path('returns/', views.returns, name='returns'),
    path('core_return_policy/', views.core_return_policy, name='core_return_policy'),
    path('return_material_request/', views.return_material_request, name='return_material_request'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)