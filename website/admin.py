from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(contact_us)
admin.site.register(newsletter)
admin.site.register(blogs)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Category)
admin.site.register(Subcategory)  
admin.site.register(Bank_details)  
admin.site.register(crypto) 
admin.site.register(order) 
admin.site.register(return_material_authorization)