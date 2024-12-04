from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse

# For API
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from swe33.models import *  
from .serializers import * 

# Create your views here.

# Existing view for the homepage
def home(request):
    return render(request, 'index.html')

# API View for Buyer
class BuyerListAPI(APIView):
    def get(self, request):
        buyers = Buyer.objects.all()
        serializer = BuyerSerializer(buyers, many=True)
        return Response(serializer.data)

# API View for Delivery
class DeliveryListAPI(APIView):
    def get(self, request):
        deliveries = Delivery.objects.all()
        serializer = DeliverySerializer(deliveries, many=True)
        return Response(serializer.data)

# API View for Farm
class FarmListAPI(APIView):
    def get(self, request):
        farms = Farm.objects.all()
        serializer = FarmSerializer(farms, many=True)
        return Response(serializer.data)

# API View for Farmer
class FarmerListAPI(APIView):
    def get(self, request):
        farmers = Farmer.objects.all()
        serializer = FarmerSerializer(farmers, many=True)
        return Response(serializer.data)

# API View for Order
class OrderListAPI(APIView):
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

# API View for OrderProduct
class OrderProductListAPI(APIView):
    def get(self, request):
        order_products = Orderproduct.objects.all()
        serializer = OrderProductSerializer(order_products, many=True)
        return Response(serializer.data)

# API View for Payment
class PaymentListAPI(APIView):
    def get(self, request):
        payments = Payment.objects.all()
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)

# API View for Product
class ProductListAPI(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    



class UserLoginAPI(APIView):
    def post(self, request):
        # Extract email, password, and user_type from the request
        email = request.data.get('email')
        password = request.data.get('password')
        user_type = request.data.get('user_type')
        name = request.data.get('name')

        if not email or not password or not user_type:
            return Response(
                {"error": "Email, password, and user_type are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate based on user_type
        if user_type.lower() == 'buyer':
            try:
                buyer = Buyer.objects.get(email=email)  # Fetch buyer from the database
                if buyer.password == password:  # Validate password
                    return Response(
                        {"message": str(buyer.buyerid), "name": buyer.name},
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {"error": "Invalid password for buyer."},
                        status=status.HTTP_401_UNAUTHORIZED
                    )
            except Buyer.DoesNotExist:
                return Response(
                    {"error": "Buyer with this email does not exist."},
                    status=status.HTTP_404_NOT_FOUND
                )

        elif user_type.lower() == 'farmer':
            try:
                farmer = Farmer.objects.get(email=email)  # Fetch farmer from the database
                if farmer.password == password:  # Validate password
                    return Response(
                        {"message": str(farmer.farmerid), "name": farmer.name},
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {"error": "Invalid password for farmer."},
                        status=status.HTTP_401_UNAUTHORIZED
                    )
            except Farmer.DoesNotExist:
                return Response(
                    {"error": "Farmer with this email does not exist."},
                    status=status.HTTP_404_NOT_FOUND
                )

        else:
            return Response(
                {"error": "Invalid user_type. It must be 'buyer' or 'farmer'."},
                status=status.HTTP_400_BAD_REQUEST
            )
        

class UserRegistrationAPI(APIView):
    def post(self, request):
        # Extract data from the request
        name = request.data.get('name')
        email = request.data.get('email')
        phone = request.data.get('phone')
        address = request.data.get('address', None) #for buyers
        farmlocation = request.data.get('farmlocation', None)  # For farmers
        password = request.data.get('password')
        user_type = request.data.get('user_type', None)  # 'buyer' or 'farmer'
        farm_size = request.data.get('farm_size', None)   # for farmer
        crop_type = request.data.get('crop_type', None)   # for farmer
        governmentid = request.data.get('governmentid', None) # for farmer
        preferred_payment_method = request.data.get('preferred_payment_method', None)#buyer

        if not all([name, email, password, user_type]):
            return Response(
                {"error": "Name, email, password, and user_type are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check user_type and handle registration
        if user_type.lower() == 'buyer':
            if Buyer.objects.filter(email=email).exists():
                return Response(
                    {"error": "Buyer with this email already exists."},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            # Create a new Buyer instance
            buyer = Buyer.objects.create(
                name=name,
                email=email,
                phone=phone,
                address=address,
                password=password,
                preferred_payment_method=preferred_payment_method
            )
            return Response(
                {"message": "Buyer registered successfully!", "buyer_id": buyer.buyerid},
                status=status.HTTP_201_CREATED
            )

        elif user_type.lower() == 'farmer':
            if Farmer.objects.filter(email=email).exists():
                return Response(
                    {"error": "Farmer with this email already exists."},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            # Create a new Farmer instance
            farmer = Farmer.objects.create(
                name=name,
                email=email,
                phone=phone,
                farmlocation=farmlocation,
                password=password,
                farm_size=farm_size,
                crop_type=crop_type,
                governmentid=governmentid
            )
            return Response(
                {"message": "Farmer registered successfully!", "farmer_id": farmer.farmerid},
                status=status.HTTP_201_CREATED
            )

        else:
            return Response(
                {"error": "Invalid user_type. It must be 'buyer' or 'farmer'."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
# ....

class FarmerProductsAPI(APIView):
    def get(self, request, id):  # 'id' is the farmer's ID from the URL
        try:
            # Check if the farmer exists
            farmer = Farmer.objects.get(pk=id)
            
            # Get all products associated with the farmer
            products = Product.objects.filter(farmerid=farmer)
            
            # Serialize the product data
            serializer = ProductSerializer(products, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Farmer.DoesNotExist:
            return Response(
                {"error": "Farmer with this ID does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )
        

class ProductDetailAPI(APIView):
    def get(self, request, id):
        try:
            # Fetch the product by ID
            product = Product.objects.get(pk=id)
            
            # Serialize the product data
            serializer = ProductSerializer(product)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product with this ID does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )
        

class DeleteProductAPI(APIView):
    def post(self, request):
        # Extract product ID from the request body
        product_id = request.data.get('id')

        if not product_id:
            return Response(
                {"error": "Product ID is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Fetch the product by ID
            product = Product.objects.get(pk=product_id)

            # Fetch and delete all OrderProduct entries associated with this product
            related_orderproducts = Orderproduct.objects.filter(productid=product_id)
            related_orderproducts.delete()

            # Delete the product itself
            product.delete()

            return Response(
                {"message": f"Product with ID {product_id} and its associated order products have been deleted successfully."},
                status=status.HTTP_200_OK
            )
        except Product.DoesNotExist:
            return Response(
                {"error": f"Product with ID {product_id} does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )
        

class UpdateProductAPI(APIView):
    def post(self, request, id):
        try:
            # Fetch the product by ID
            product = Product.objects.get(pk=id)

            # Check if required fields are provided and valid
            if not request.data.get('name') or not request.data.get('price') or not request.data.get('quantity'):
                return Response(
                    {"error": "Name, price, and quantity are required and cannot be empty."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Update fields from the request data (if provided)
            product.name = request.data.get('name', product.name)
            product.price = request.data.get('price', product.price)
            product.quantity = request.data.get('quantity', product.quantity)
            product.image = request.data.get('image', product.image)

            # Save the updated product
            product.save()

            return Response(
                {"message": f"Product with ID {id} has been updated successfully."},
                status=status.HTTP_200_OK
            )
        except Product.DoesNotExist:
            return Response(
                {"error": f"Product with ID {id} does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )
        

class AddProductAPI(APIView):
    def post(self, request):
        # Extract data from the request
        farmer_id = request.data.get('farmer_id')  # Farmer ID to associate the product with
        name = request.data.get('name')
        price = request.data.get('price')
        quantity = request.data.get('quantity')
        image = request.data.get('image', None)  # Optional field

        if not farmer_id or not name or not price or not quantity:
            return Response(
                {"error": "Farmer ID, name, price, and quantity are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Fetch the farmer by ID
            farmer = Farmer.objects.get(pk=farmer_id)

            # Check if the farmer has a farm
            farm = Farm.objects.filter(farmerid=farmer).first()
            

            # Create a new product and associate it with the farm
            product = Product.objects.create(
                farmerid = farmer,
                name=name,
                price=price,
                quantity=quantity,
                image=image,
                farmid = farm,
            )

            return Response(
                {"message": "Product added successfully.", "product_id": product.productid},
                status=status.HTTP_201_CREATED
            )
        except Farmer.DoesNotExist:
            return Response(
                {"error": f"Farmer with ID {farmer_id} does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )
        

class AddToCartView(APIView):
    def post(self, request):
        # Extract data from the request
        product_id = request.data.get('productid')
        product_name = request.data.get('productname')
        product_price = request.data.get('price')
        buyer_id = request.data.get('buyerid')
        quantity = request.data.get('quantity')
        farmer_id = request.data.get('farmerid')
        status_value = request.data.get('status')

        # Validate required fields
        if not all([product_id, product_name, product_price, buyer_id, quantity, farmer_id, status_value]):
            return Response(
                {"error": "Missing required fields."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Validate if Product, Buyer, and Farmer exist
            product = Product.objects.get(pk=product_id)
            buyer = Buyer.objects.get(pk=buyer_id)
            farmer = Farmer.objects.get(pk=farmer_id)

            # Validate product name and price match the product
            

            # Check if the product already exists in the cart for the buyer
            existing_cart_item = Cart.objects.filter(
                productid=product, buyerid=buyer, farmerid=farmer
            ).first()

            if existing_cart_item:
                # Update the quantity of the existing cart item
                existing_cart_item.quantity += quantity
                existing_cart_item.save()
                return Response(
                    {
                        "message": "Cart updated successfully.",
                        "cart": {
                            "cartid": existing_cart_item.cartid,
                            "productid": product_id,
                            "productname": product_name,
                            "productprice": product_price,
                            "buyerid": buyer_id,
                            "quantity": existing_cart_item.quantity,
                            "farmerid": farmer_id,
                            "status": status_value,
                        }
                    },
                    status=status.HTTP_200_OK
                )

            # Create a new Cart instance if the product does not already exist
            cart = Cart.objects.create(
                productid=product,
                buyerid=buyer,
                farmerid=farmer,
                quantity=quantity,
                status=status_value,
                productname=product_name,  # Ensure these fields exist in the Cart model
                price=product_price,
            )

            return Response(
                {
                    "message": "Product successfully added to cart.",
                    "cart": {
                        "cartid": cart.cartid,
                        "productid": product_id,
                        "productname": product_name,
                        "productprice": product_price,
                        "buyerid": buyer_id,
                        "quantity": quantity,
                        "farmerid": farmer_id,
                        "status": status_value,
                    }
                },
                status=status.HTTP_201_CREATED
            )

        except Product.DoesNotExist:
            return Response(
                {"error": f"Product with ID {product_id} does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Buyer.DoesNotExist:
            return Response(
                {"error": f"Buyer with ID {buyer_id} does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Farmer.DoesNotExist:
            return Response(
                {"error": f"Farmer with ID {farmer_id} does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )


class DeleteCartItemView(APIView):
    def post(self, request, id):
        try:
            # Fetch the cart item by ID
            cart_item = Cart.objects.get(pk=id)

            # Delete the cart item
            cart_item.delete()

            return Response(
                {"message": f"Cart item with ID {id} has been deleted successfully."},
                status=status.HTTP_200_OK
            )

        except Cart.DoesNotExist:
            return Response(
                {"error": f"Cart item with ID {id} does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )


class AddOrderView(APIView):
    def post(self, request):
        # Extract data from the request
        farmer_id = request.data.get('farmerid')
        buyer_id = request.data.get('buyerid')
        order_date = request.data.get('orderdate')
        order_status = request.data.get('orderstatus')
        total_amount = request.data.get('totalamount')
        total_price = request.data.get('totalprice')
        product_name = request.data.get('productname')

        # Validate required fields
        if not all([farmer_id, buyer_id, order_date, order_status, total_amount, total_price, product_name]):
            return Response(
                {"error": "Missing required fields."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Validate if Farmer and Buyer exist
            farmer = Farmer.objects.get(pk=farmer_id)
            buyer = Buyer.objects.get(pk=buyer_id)

            # Parse order_date if provided
            try:
                order_date_parsed = datetime.strptime(order_date, "%Y-%m-%d").date()
            except ValueError:
                return Response(
                    {"error": "Invalid date format. Expected 'yyyy-MM-dd'."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create and save the order
            order = Order.objects.create(
                farmerid=farmer_id,
                buyerid=buyer,
                orderdate=order_date_parsed,
                orderstatus=order_status,
                totalamount=total_amount,
                totalprice=total_price,
                productname=product_name,  # Ensure this field exists in your Order model
            )

            return Response(
                {
                    "message": "Order created successfully.",
                    "order": {
                        "orderid": order.orderid,
                        "farmerid": farmer_id,
                        "buyerid": buyer_id,
                        "orderdate": str(order_date_parsed),
                        "orderstatus": order_status,
                        "totalamount": total_amount,
                        "totalprice": total_price,
                        "productname": product_name,
                    },
                },
                status=status.HTTP_201_CREATED
            )

        except Farmer.DoesNotExist:
            return Response(
                {"error": f"Farmer with ID {farmer_id} does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Buyer.DoesNotExist:
            return Response(
                {"error": f"Buyer with ID {buyer_id} does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )


class GetOrdersView(APIView):
    def get(self, request, buyerid, userType):
        try:
            # Validate userType and fetch orders accordingly
            if userType.lower() == "buyer":
                buyer = Buyer.objects.get(pk=buyerid)
                orders = Order.objects.filter(buyerid=buyer)
            elif userType.lower() == "farmer":
                farmer = Farmer.objects.get(pk=buyerid)  # buyerid here refers to farmerid
                orders = Order.objects.filter(farmerid=buyerid)
            else:
                return Response(
                    [{"error": "Invalid userType. Must be 'buyer' or 'farmer'."}],
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Check if orders exist
            if not orders.exists():
                return Response([], status=status.HTTP_200_OK)  # Return an empty list if no orders found

            # Serialize the orders and return them
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Buyer.DoesNotExist:
            return Response(
                [{"error": f"Buyer with ID {buyerid} does not exist."}],
                status=status.HTTP_404_NOT_FOUND
            )
        except Farmer.DoesNotExist:
            return Response(
                [{"error": f"Farmer with ID {buyerid} does not exist."}],
                status=status.HTTP_404_NOT_FOUND
            )
        

class DeleteOrderView(APIView):
    def post(self, request, id):
        try:
            # Fetch the order by ID
            order = Order.objects.get(pk=id)

            # Delete the order
            order.delete()

            return Response(
                {"message": f"Order with ID {id} has been deleted successfully."},
                status=status.HTTP_200_OK
            )

        except Order.DoesNotExist:
            return Response(
                {"error": f"Order with ID {id} does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )
        

class UpdateOrderView(APIView):
    def post(self, request):
        # Extract data from the request body
        order_id = request.data.get('orderid')
        farmer_id = request.data.get('farmerid')
        buyer_id = request.data.get('buyerid')
        order_date = request.data.get('orderdate')
        order_status = request.data.get('orderstatus')
        total_amount = request.data.get('totalamount')
        total_price = request.data.get('totalprice')
        product_name = request.data.get('productname')

        # Validate required fields
        if not order_id:
            return Response(
                {"error": "Order ID is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Fetch the order by ID
            order = Order.objects.get(pk=order_id)

            # Update fields if provided
            if farmer_id:
                order.farmerid_id = farmer_id  # Use `_id` to set the foreign key
            if buyer_id:
                order.buyerid_id = buyer_id  # Use `_id` to set the foreign key
            if order_date:
                try:
                    order.orderdate = datetime.strptime(order_date, "%Y-%m-%d").date()
                except ValueError:
                    return Response(
                        {"error": "Invalid date format. Expected 'yyyy-MM-dd'."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            if order_status:
                order.orderstatus = order_status
            if total_amount is not None:
                order.totalamount = total_amount
            if total_price is not None:
                order.totalprice = total_price
            if product_name:
                order.productname = product_name

            # Save the updated order
            order.save()

            return Response(
                {"message": f"Order with ID {order_id} has been updated successfully."},
                status=status.HTTP_200_OK
            )

        except Order.DoesNotExist:
            return Response(
                {"error": f"Order with ID {order_id} does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )


class CartByBuyerView(APIView):
    def get(self, request, buyerid):
        try:
            # Check if the buyer exists
            buyer = Buyer.objects.get(pk=buyerid)
        except Buyer.DoesNotExist:
            return Response(
                {"error": f"Buyer with ID {buyerid} does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Fetch all cart items for the given buyer
        cart_items = Cart.objects.filter(buyerid=buyer)

        # If no cart items are found
        if not cart_items.exists():
            return Response(
                {"message": "No products in the cart for this buyer."},
                status=status.HTTP_200_OK
            )

        # Serialize the cart items
        serializer = CartSerializer(cart_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class UserChatsView(APIView):
    def get(self, request, userId, usertype):
        try:
            # Validate usertype and fetch the user
            if usertype.lower() == "buyer":
                user = Buyer.objects.get(pk=userId)
                chats = Chat.objects.filter(buyerid=user)
            elif usertype.lower() == "farmer":
                user = Farmer.objects.get(pk=userId)
                chats = Chat.objects.filter(farmerid=user)
            else:
                return Response(
                    [{"error": "Invalid usertype. Must be 'buyer' or 'farmer'."}],  # Array response
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Check if chats exist
            if not chats.exists():
                return Response(
                    [],  # Return an empty array for no chats
                    status=status.HTTP_200_OK
                )

            # Serialize the chat data
            serializer = ChatSerializer(chats, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Buyer.DoesNotExist:
            return Response(
                [{"error": f"Buyer with ID {userId} does not exist."}],  # Array response
                status=status.HTTP_404_NOT_FOUND
            )
        except Farmer.DoesNotExist:
            return Response(
                [{"error": f"Farmer with ID {userId} does not exist."}],  # Array response
                status=status.HTTP_404_NOT_FOUND
            )
        

class FarmerNameView(APIView):
    def get(self, request, id):
        try:
            # Fetch the farmer by ID
            farmer = Farmer.objects.get(pk=id)
            
            # Return the farmer's name in the response
            return Response(
                {"name": farmer.name},
                status=status.HTTP_200_OK
            )
        except Farmer.DoesNotExist:
            # Return an error if the farmer does not exist
            return Response(
                {"error": f"Farmer with ID {id} does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )
        
class BuyerNameView(APIView):
    def get(self, request, id):
        try:
            # Fetch the buyer by ID
            buyer = Buyer.objects.get(pk=id)
            
            # Return the buyer's name in the response
            return Response(
                {"name": buyer.name},
                status=status.HTTP_200_OK
            )
        except Buyer.DoesNotExist:
            # Return an error if the buyer does not exist
            return Response(
                {"error": f"Buyer with ID {id} does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )
        

class SendMessageView(APIView):
    def post(self, request):
        # Extract data from the request body
        chat_id = request.data.get('chatid')
        sender_type = request.data.get('sendertype')
        message_text = request.data.get('messagetext')

        if not all([chat_id, sender_type, message_text]):
            return Response(
                {"error": "chatid, sendertype, and messagetext are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Ensure the chat exists
            chat = Chat.objects.get(pk=chat_id)

            # Create and save the message
            message = Message.objects.create(
                chatid=chat,
                sendertype=sender_type,
                messagetext=message_text,
                sentat=datetime.now()
            )

            return Response(
                {"message": "Message sent successfully."},
                status=status.HTTP_201_CREATED
            )

        except Chat.DoesNotExist:
            return Response(
                {"error": f"Chat with ID {chat_id} does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )
        

class SendChatView(APIView):
    def post(self, request):
        # Extract data from the request body
        buyer_id = request.data.get('buyerid')
        farmer_id = request.data.get('farmerid')
        status_value = request.data.get('status')

        if not all([buyer_id, farmer_id, status_value]):
            return Response(
                {"error": "buyerid, farmerid, and status are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Ensure the buyer and farmer exist
            buyer = Buyer.objects.get(pk=buyer_id)
            farmer = Farmer.objects.get(pk=farmer_id)

            # Check if a chat already exists between the buyer and farmer
            existing_chat = Chat.objects.filter(buyerid=buyer, farmerid=farmer).first()
            if existing_chat:
                return Response(
                    {"error": "A chat already exists between this buyer and farmer."},
                    status=status.HTTP_409_CONFLICT  # HTTP 409 Conflict
                )

            # Create and save the chat
            chat = Chat.objects.create(
                buyerid=buyer,
                farmerid=farmer,
                status=status_value,
                createdat=datetime.now()
            )

            return Response(
                {"message": "Chat created successfully."},
                status=status.HTTP_201_CREATED
            )

        except Buyer.DoesNotExist:
            return Response(
                {"error": f"Buyer with ID {buyer_id} does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Farmer.DoesNotExist:
            return Response(
                {"error": f"Farmer with ID {farmer_id} does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )
        

class GetChatMessagesView(APIView):
    def get(self, request, chatId):
        try:
            # Ensure the chat exists
            chat = Chat.objects.get(pk=chatId)

            # Fetch all messages for the chat, sorted by 'sentat'
            messages = Message.objects.filter(chatid=chat).order_by('sentat')

            # Check if messages exist
            if not messages.exists():
                return Response(
                    {"message": "No messages found for this chat."},
                    status=status.HTTP_200_OK
                )

            # Serialize and return the messages
            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Chat.DoesNotExist:
            return Response(
                {"error": f"Chat with ID {chatId} does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )
        

# ....

