from django.db.models import Q 
from atributes.models import Cheveux, Tag
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse, request
from .forms import ContactForm
from delivery.models import Wilaya, Commune
from django.views.generic import TemplateView, DetailView, ListView, CreateView, View
from .models import Product, Category
from business.models import Business, ThreePhotos, Slide, DualBanner, Counter, LargeBanner
from cart.forms import CartAddProductForm
from business.models import Counter
from .filters import ProductFilter
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["new_products"] = Product.objects.filter(top=True)
        context["top_products"] = Product.objects.filter(top=True)
        context["big_slides"] = Slide.objects.all()
        context["three_photos"] = ThreePhotos.objects.all()[:3]
        context["dual_banners"] = DualBanner.objects.all()[:2]
        context["large_banner"] = LargeBanner.objects.last()
        context["random_cat"] = Category.objects.all()
        all_cat = Category.objects.all()
        cat_list = []
        for cat in all_cat:
            if cat.products.all().count() > 0:
                cat_list.append(cat)
        print('categories ', cat_list)
        context["random_cat"] = cat_list[:3]
        print('a tchou hadi', context["random_cat"])
        return context
#  STATIC

class AboutView(TemplateView):
    template_name = "about.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["counters"] = Counter.objects.all()[:4]
        return context

class VirementBancaireView(TemplateView):
    template_name = "paiement/virement-bancaire.html"

class CarteBancaireView(TemplateView):
    template_name = "paiement/carte-bancaire.html"

class PaiementView(TemplateView):
    template_name = "paiement/paiement.html"

class PaiementEspecesView(TemplateView):
    template_name = "paiement/paiement-especes.html"


#  LIVRAISON

class EchangeView(TemplateView):
    template_name = "livraison/echange.html"

class LivraisonView(TemplateView):
    template_name = "livraison/livraison.html"

class RetourView(TemplateView):
    template_name = "livraison/retours.html"


def product_detail(request):
    product = Product.objects.get(id=Product.objects.first().id)
    return render(request, 'snipetts/product-modal.html', {'product': product})

# class CategoryProductsView(ListView):
#     context_object_name = 'products'
#     model = Product
#     paginate_by = 15
#     template_name = "products.html"

#     def get_queryset(self, *args, **kwargs): # new
        
#         products = Product.objects.filter(actif=True)
#         try:
#             category = get_object_or_404(Category, slug=self.kwargs['slug'])
#             products = products.filter(category__category=category)
#         except:
#             products = products.filter(category=category)
#         return products
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["categories"] = Category.objects.all()
#         # context["products"] = Product.objects.all()
#         return context



# for django-filter pagination MABE
class PaginatedFilterViews(View):
    def get_context_data(self, **kwargs):
        context = super(PaginatedFilterViews, self).get_context_data(**kwargs)
        if self.request.GET:
            querystring = self.request.GET.copy()
            if self.request.GET.get('page'):
                del querystring['page']
            context['querystring'] = querystring.urlencode()
        return context



class ProductsView(PaginatedFilterViews, ListView):
    context_object_name = 'products'
    model = Product
    template_name = "products.html"
    def get_queryset(self):
        try:
            param = self.request.GET.get('category')
            category = Category.objects.get(id = param)
            products = Product.objects.filter(category__in=category.get_descendants(include_self=True))
            print('les produits ', products)
            return products
        except:
            return super().get_queryset() 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get('category'):
            param = self.request.GET.get('category')
            context["category"] = Category.objects.get(id = param)
        context["tags"] = Tag.objects.all()
        # context["products"] = Product.objects.all()
        return context



def filtered_view(request):
    # filter = ProductFilter(request.GET, queryset= Product.objects.all())
    html = render_to_string('snipetts/ajax-product-block.html', {'filter': filter}, request=request)
    # paginator = Paginator(filter.qs, 4)
    # page = request.GET.get('page')
    # try:
    #     products = paginator.page(page)
    # except PageNotAnInteger:
    #     products = paginator.page(1)
    # except EmptyPage:
    #     products = paginator.page(paginator.num_pages)
    return JsonResponse({'form': html})

# class ProductsView(ListView):
#     context_object_name = 'products'
#     model = Product
#     paginate_by = 15
#     template_name = "products.html"

#     def get_queryset(self): # new
#         query = self.request.GET.get('q')
#         min = self.request.GET.get('min')
#         max = self.request.GET.get('max')
#         new = self.request.GET.get('new')
#         top = self.request.GET.get('top')
#         if max and new and top:
#             products = Product.objects.filter(price__range=[min, max], actif=True, new= True, top=True)
#         elif max and new:
#             products = Product.objects.filter(price__range=[min, max], actif=True,new= True)
#         elif max and top:
#             products = Product.objects.filter(price__range=[min, max], actif=True, top=True)
#         elif top and new:
#             products = Product.objects.filter(actif=True,new= True, top=True)
#         elif max:
#             products = Product.objects.filter(price__range=[min, max], actif=True)
#         elif new:
#             products = Product.objects.filter(actif=True,new= True)
#         elif top:
#             products = Product.objects.filter(actif=True, top=True)
#         elif query:
#             if len(query) > 2:
#                 by_2 = [query[i:i+2] for i in range(0, len(query), 2)][0]
#                 by_1 = [query[i:i+2] for i in range(0, len(query), 2)][1:]
#                 print('the sring split one  ', by_2)
#                 print('the sring towo', by_1)
#                 for i in by_1:
#                     products = Product.objects.filter(
#                             Q(name__icontains=by_2) & Q(name__icontains=i)
#                             )
#                     if not len(products):
#                         products = Product.objects.filter(
#                             Q(name__icontains=by_2) | Q(name__icontains=i)
#                             )
#             else: 
#                 products = Product.objects.filter(name__icontains=query)
#         else :
#             products = Product.objects.all()
#         return products

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # context["categories"] = Category.objects.all()
#         context["sous_categories"] = SubCategory.objects.all()
#         # context["products"] = Product.objects.all()
#         return context



class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = "product-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["related"] = Product.objects.all().order_by('?')[:4] 
        context["wilayas"] = Wilaya.objects.all().order_by('name') 
        prod = self.get_object()
        category = prod.category
        products =  Product.objects.filter(category = category)
        context["related_products"] = products.exclude(id= prod.id).order_by('?')[:8]
        context["related_products_count"] = products.count() - 1
        return context
    


class ContactView(CreateView):
    template_name = 'contact.html'
    form_class = ContactForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
  
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
      
        message = 'Une erreur est survenue, veuillez réessayer.'
        success = False
        try:
            #save the form   
            if form.is_valid():
                form.save()
                #messages.success(request, 'Votre message a bien été envoyé')
                message = 'Votre message a bien été envoyé!'
                success = True
                print(success)
                return render(request, 'other/contact.html', {'message': message, 'success': success})
            else:
                print(success)
                message = 'Une erreur est survenue, veuillez réessayer.'
                return render(request, 'contact.html', {'message': message, 'failure': True})
        except:
            return render(request, 'contact.html', {'message': message, 'failure': True})
        return render(request, 'contact.html', {'message': message, 'failure': True})




