from .models import Category
from itertools import chain

def trees(request):
    categories = Category.objects.filter(level=0, actif=True)
    context = {
        'categories' : categories,
        'bottom_categories' : categories.order_by('?')[:7],
    }
    return context


