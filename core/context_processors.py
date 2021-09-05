from .models import Category
from itertools import chain

def trees(request):
    categories = Category.objects.filter(level=0)
    context = {
            'categories' : categories,
    }
    return context
    

