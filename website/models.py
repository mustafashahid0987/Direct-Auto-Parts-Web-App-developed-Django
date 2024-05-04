from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from ckeditor.fields import RichTextField

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    street_address_1 = models.CharField(max_length=255)
    street_address_2 = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.user
    
class contact_us(models.Model):
    submission_date = models.DateField(default=datetime.now, blank=True)
    first_name = models.CharField(max_length=1000000000,null=True)
    last_name = models.CharField(max_length=1000000000,null=True)
    email = models.CharField(max_length=1000000000,null=True)
    subject = models.CharField(max_length=1000000000,null=True)
    message = models.CharField(max_length=1000000000,null=True)

    def __str__(self):
        return self.first_name
    
# Create your models here.
class return_material_authorization(models.Model):
    submission_date = models.DateField(default=datetime.now, blank=True)
    name = models.CharField(max_length=1000000000,null=True)
    email = models.CharField(max_length=1000000000,null=True)
    phone = models.CharField(max_length=1000000000,null=True)
    order_no = models.CharField(max_length=1000000000,null=True)
    notes = models.CharField(max_length=1000000000,null=True)

    def __str__(self):
        return (str(self.name))
    

class newsletter(models.Model):

    ndate = models.DateField(auto_now_add=True)
    email = models.CharField(max_length=1000000000,null=True)

    def __str__(self):
        return (str(self.ndate))
    

class blogs(models.Model):
    submission_date = models.DateField(default=datetime.now, blank=True)
    title = models.CharField(max_length=1000000000,null=True)
    content = models.CharField(max_length=1000000000,null=True)
    image_file = models.ImageField(upload_to='media',null=True,default="None")
    
    def __str__(self):
        return (str(self.title))
    

class Category(models.Model):
    name = models.CharField(max_length=1000000000,null=True)
    image_file = models.ImageField(upload_to='media',null=True,default="None")

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    name = models.CharField(max_length=1000000000,null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    submission_date = models.DateField(default=datetime.now, blank=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    # Add other fields for product details
    
    name = models.CharField(max_length=1000000000,null=True)
    desc = RichTextField()
    price = models.FloatField(max_length=1000000000,null=True)
    quantity = models.IntegerField(null=True)

    def __str__(self):
        return self.name
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image_file = models.ImageField(upload_to='product_images')

    def __str__(self):
        return f"Image for {self.product.name}"

class addtocart(models.Model):
    user_id = models.CharField(max_length=20,default='none')
    coin_ids = models.ManyToManyField(Product)
    quantity = models.IntegerField(null=True)


class watchlist(models.Model):
    user_id = models.CharField(max_length=20,default='none')
    coin_ids = models.ManyToManyField(Product)

class order(models.Model):
    order_status = [
    ('Paid', 'Paid'),
    ('Unpaid', 'Unpaid'),

]
    fulfilment_status = [
    ('Fulfilled', 'Fulfilled'),
    ('Unfulfilled', 'Unfulfilled'),

]
    order_date = models.DateField(default=datetime.now, blank=True)
    user_id = models.CharField(max_length=20,default='none')
    coin_ids = models.ManyToManyField(Product)
    payment_proof = models.ImageField(upload_to='media',null=True)
    status = models.CharField(max_length=1000000000,choices=order_status,null=True)
    fulfilment_status = models.CharField(max_length=1000000000,choices=fulfilment_status,null=True)
    first_name = models.CharField(max_length=1000000000,null=True)
    last_name = models.CharField(max_length=1000000000,null=True)
    email = models.CharField(max_length=1000000000,null=True)
    phone_no = models.CharField(max_length=1000000000,null=True)
    address = models.CharField(max_length=1000000000,null=True)
    country = models.CharField(max_length=1000000000,null=True)
    postal_code = models.CharField(max_length=1000000000,null=True)
    price = models.FloatField(max_length=1000000000,null=True)


class Bank_details(models.Model):
    first_name = models.CharField(max_length=1000000000,null=True)
    last_name = models.CharField(max_length=1000000000,null=True)
    bank_name = models.CharField(max_length=1000000000,null=True)
    account_no = models.CharField(max_length=1000000000,null=True)

    def __str__(self):
        return (self.bank_name)
    

class crypto(models.Model):

    network = models.CharField(max_length=1000000000,null=True)
    wallet_address = models.CharField(max_length=1000000000,null=True)
    

    def __str__(self):
        return (self.network)
    

class discount_table(models.Model):
    user_ids = models.OneToOneField(User, on_delete=models.CASCADE)
    discount = models.CharField(max_length=1000000000,null=True)
    order_limit = models.IntegerField(null=True)