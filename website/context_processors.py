from .models import *

def categories(request):
    # Fetch and return all categories
    cat = Category.objects.all()
    subcat = Subcategory.objects.all()

    return {'categories':cat, 'subcat':subcat,}