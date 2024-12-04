from django.urls import path
from . import views  # Importing your views
from .views import *

urlpatterns = [
    path('', home, name='home'),  # Homepage route
    path('api/buyers/', BuyerListAPI.as_view(), name='buyer_list_api'),  # Buyer API
    path('api/deliveries/', DeliveryListAPI.as_view(), name='delivery_list_api'),  # Delivery API
    path('api/farms/', FarmListAPI.as_view(), name='farm_list_api'),  # Farm API
    path('api/farmers/', FarmerListAPI.as_view(), name='farmer_list_api'),  # Farmer API
    path('api/orders/', OrderListAPI.as_view(), name='order_list_api'),  # Order API
    path('api/order-products/', OrderProductListAPI.as_view(), name='order_product_list_api'),  # OrderProduct API
    path('api/payments/', PaymentListAPI.as_view(), name='payment_list_api'),  # Payment API
    path('api/products/', ProductListAPI.as_view(), name='product_list_api'),  # Product API


    path('api/login/', UserLoginAPI.as_view(), name='user_login_api'),  # Add this line
    path('api/register/', UserRegistrationAPI.as_view(),name='user_registration_api'),


    #....

    path('api/farmer/<int:id>/products/', FarmerProductsAPI.as_view(), name='farmer_products_api'),

    path('api/product/<int:id>/', ProductDetailAPI.as_view(), name='product_detail_api'),

    path('api/deleteproduct/', DeleteProductAPI.as_view(), name='delete_product_api'),

    path('api/product/<int:id>/update/', UpdateProductAPI.as_view(), name='update_product_api'),

    path('api/farmer/product/add/', AddProductAPI.as_view(), name='add_product_api'),

    # ...

    path('api/product/add/cart/', AddToCartView.as_view(), name='add_to_cart'),
    
    path('api/product/cart/<int:buyerid>/', CartByBuyerView.as_view(), name='cart_by_buyer'),

    path('api/buyer/chats/<int:userId>/<str:usertype>/', UserChatsView.as_view(), name='user_chats'),

    path('api/farmer/name/<int:id>/', FarmerNameView.as_view(), name='get_farmer_name'),

    path('api/buyer/name/<int:id>/', BuyerNameView.as_view(), name='get_buyer_name'),


    path('api/send/message/', SendMessageView.as_view(), name='send_message'),
    path('api/send/chat/', SendChatView.as_view(), name='send_chat'),
    path('api/chat/<int:chatId>/messages/', GetChatMessagesView.as_view(), name='get_chat_messages'),


    path('api/delete/cart/item/<int:id>/', DeleteCartItemView.as_view(), name='delete_cart_item'),

    path('api/add/order/', AddOrderView.as_view(), name='add_order'),

    path('api/order/<int:buyerid>/<str:userType>/', GetOrdersView.as_view(), name='get_orders'),

    path('api/delete/order/<int:id>/', DeleteOrderView.as_view(), name='delete_order'),

    path('api/update/order/', UpdateOrderView.as_view(), name='update_order'),


]