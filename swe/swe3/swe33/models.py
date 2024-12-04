from django.db import models

class Buyer(models.Model):
    buyerid = models.AutoField(db_column='BuyerID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=50)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=50)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=15, blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=100, blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(max_length=20)
    image = models.CharField(max_length=255, blank=True, null=True)
    preferred_payment_method = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'buyer'


class Cart(models.Model):
    cartid = models.AutoField(db_column='CartID', primary_key=True)  # Field name made lowercase.
    buyerid = models.ForeignKey(Buyer, models.DO_NOTHING, db_column='BuyerID')  # Field name made lowercase.
    productid = models.ForeignKey('Product', models.DO_NOTHING, db_column='ProductID')  # Field name made lowercase.
    farmerid = models.ForeignKey('Farmer', models.DO_NOTHING, db_column='FarmerID')  # Field name made lowercase.
    quantity = models.IntegerField(db_column='Quantity')  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=11, blank=True, null=True)  # Field name made lowercase.
    addeddate = models.DateTimeField(db_column='AddedDate', blank=True, null=True)  # Field name made lowercase.
    price = models.DecimalField(db_column='Price', max_digits=10, decimal_places=2)  # Field name made lowercase.
    productname = models.CharField(db_column='ProductName', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'cart'


class Chat(models.Model):
    chatid = models.AutoField(db_column='ChatID', primary_key=True)  # Field name made lowercase.
    buyerid = models.ForeignKey(Buyer, models.DO_NOTHING, db_column='BuyerID')  # Field name made lowercase.
    farmerid = models.ForeignKey('Farmer', models.DO_NOTHING, db_column='FarmerID')  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=6, blank=True, null=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='CreatedAt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'chat'


class Delivery(models.Model):
    deliveryid = models.AutoField(db_column='DeliveryID', primary_key=True)  # Field name made lowercase.
    orderid = models.ForeignKey('Order', models.DO_NOTHING, db_column='OrderID', blank=True, null=True)  # Field name made lowercase.
    deliverydate = models.DateField(db_column='DeliveryDate', blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=100, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'delivery'




class Farm(models.Model):
    farmid = models.AutoField(db_column='FarmID', primary_key=True)  # Field name made lowercase.
    farmerid = models.ForeignKey('Farmer', models.DO_NOTHING, db_column='FarmerID', blank=True, null=True)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=100, blank=True, null=True)  # Field name made lowercase.
    size = models.DecimalField(db_column='Size', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    crop_type = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'farm'


class Farmer(models.Model):
    farmerid = models.AutoField(db_column='FarmerID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=50)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=50)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=15, blank=True, null=True)  # Field name made lowercase.
    farmlocation = models.CharField(db_column='FarmLocation', max_length=100, blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(max_length=20)
    image = models.CharField(max_length=255, blank=True, null=True)
    farm_size = models.FloatField(blank=True, null=True)
    crop_type = models.CharField(max_length=10, blank=True, null=True)
    governmentid = models.CharField(db_column='governmentID', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'farmer'


class Message(models.Model):
    messageid = models.AutoField(db_column='MessageID', primary_key=True)  # Field name made lowercase.
    chatid = models.ForeignKey(Chat, models.DO_NOTHING, db_column='ChatID')  # Field name made lowercase.
    sendertype = models.CharField(db_column='SenderType', max_length=6)  # Field name made lowercase.
    messagetext = models.TextField(db_column='MessageText')  # Field name made lowercase.
    sentat = models.DateTimeField(db_column='SentAt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'message'


class Order(models.Model):
    orderid = models.AutoField(db_column='OrderID', primary_key=True)  # Field name made lowercase.
    buyerid = models.ForeignKey(Buyer, models.DO_NOTHING, db_column='BuyerID', blank=True, null=True)  # Field name made lowercase.
    orderdate = models.DateField(db_column='OrderDate')  # Field name made lowercase.
    orderstatus = models.CharField(db_column='OrderStatus', max_length=20, blank=True, null=True)  # Field name made lowercase.
    totalprice = models.IntegerField(db_column='TotalPrice', blank=True, null=True)  # Field name made lowercase.
    farmerid = models.IntegerField(db_column='FarmerId', blank=True, null=True)  # Field name made lowercase.
    productname = models.CharField(db_column='ProductName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    totalamount = models.IntegerField(db_column='TotalAmount', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'order'


class Orderproduct(models.Model):
    orderid = models.OneToOneField(Order, models.DO_NOTHING, db_column='OrderID', primary_key=True)  # Field name made lowercase. The composite primary key (OrderID, ProductID) found, that is not supported. The first column is selected.
    productid = models.ForeignKey('Product', models.DO_NOTHING, db_column='ProductID')  # Field name made lowercase.
    quantity = models.IntegerField(db_column='Quantity', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'orderproduct'
        unique_together = (('orderid', 'productid'),)


class Payment(models.Model):
    paymentid = models.AutoField(db_column='PaymentID', primary_key=True)  # Field name made lowercase.
    orderid = models.ForeignKey(Order, models.DO_NOTHING, db_column='OrderID', blank=True, null=True)  # Field name made lowercase.
    amount = models.DecimalField(db_column='Amount', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    paymentdate = models.DateField(db_column='PaymentDate', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'payment'


class Product(models.Model):
    productid = models.AutoField(db_column='ProductID', primary_key=True)  # Field name made lowercase.
    farmid = models.ForeignKey(Farm, models.DO_NOTHING, db_column='FarmID', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=50)  # Field name made lowercase.
    price = models.DecimalField(db_column='Price', max_digits=10, decimal_places=2)  # Field name made lowercase.
    quantity = models.IntegerField(db_column='Quantity')  # Field name made lowercase.
    image = models.CharField(max_length=255, blank=True, null=True)
    farmerid = models.ForeignKey(Farmer, models.DO_NOTHING, db_column='FarmerID', blank=True, null=True)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=100, blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product'