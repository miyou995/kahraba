from django.db.models import Q
from django.http.response import HttpResponse 
from atributes.models import Tag
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse, request
from .forms import ContactForm
from delivery.models import Wilaya, Commune
from django.views.generic import TemplateView, DetailView, ListView, CreateView, View
from .models import Brand, Gamme, Product, Category
from business.models import Business, ThreePhotos, Slide, DualBanner, Counter, LargeBanner
from cart.forms import CartAddProductForm
from business.models import Counter
from .filters import ProductFilter
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from cart.forms import CartAddProductForm
from django.db.models import F
from django.core.management.utils import get_random_secret_key


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["new_products"] = Product.objects.filter(new=True, actif=True)
        context["top_products"] = Product.objects.filter(top=True, actif=True)
        context["big_slides"]   = Slide.objects.filter(actif=True)
        context["three_photos"] = ThreePhotos.objects.all()[:3]
        context["dual_banners"] = DualBanner.objects.all()[:2]
        context["large_banner"] = LargeBanner.objects.last()
        context["random_cat"]   = Category.objects.filter(actif=True)
        print(get_random_secret_key())
        all_cat = Category.objects.filter(actif=True)
        cat_list = []
        for cat in all_cat:
            if cat.products.all().count() > 0:
                cat_list.append(cat)
        print('categories ', cat_list)
        context["random_cat"] = cat_list[:3]
        print('a tchou hadi', context["random_cat"])
        return context


class AboutView(TemplateView):
    template_name = "about.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["counters"] = Counter.objects.filter(actif=True)[:4]
        return context

class VirementBancaireView(TemplateView):
    template_name = "paiement/virement-bancaire.html"

class CarteBancaireView(TemplateView):
    template_name = "paiement/carte-bancaire.html"

class PaiementView(TemplateView):
    template_name = "paiement/paiement.html"

class PaiementEspecesView(TemplateView):
    template_name = "paiement/paiement-especes.html"



class EchangeView(TemplateView):
    template_name = "livraison/echange.html"

class LivraisonView(TemplateView):
    template_name = "livraison/livraison.html"

class RetourView(TemplateView):
    template_name = "livraison/retours.html"


def product_detail(request):
    product = Product.objects.get(id=Product.objects.first().id)
    return render(request, 'snippets/product-modal.html', {'product': product})


class ProductsView(ListView):
    context_object_name = 'products'
    model = Product
    template_name = "products.html"
    paginate_by = 24
    def get_queryset(self):
        try:
            param = self.request.GET.get('category')
            # print('category', param)
            if param == 'all':
                category = Category.objects.filter(actif=True)
                products = Product.objects.filter(actif=True)
            elif param is None:
                category = Category.objects.filter(actif=True)
                products = Product.objects.filter(actif=True)
            else:
                category = Category.objects.get(id = param)
                products = Product.objects.filter(category__in=category.get_descendants(include_self=True))
        except:
            try:
                new = self.request.GET.get('new')
                if new == 'new':
                    products = Product.objects.filter(new=True)
                elif new == 'promo':
                    products = Product.objects.filter(old_price=True)
                else:
                    pass
            except:
                category = Category.objects.filter(actif=True)
                products = Product.objects.filter(actif=True)
        query = self.request.GET.get('name')
        if query:
            # print('query', query)
            qs = products.search(query=query)
            # print('les produits ')
        else:
            # print('les ELSEEEE ', products)
            qs = products
        return qs
        # except:
        #     print(' kamel les produits kharjou :) excepty !!!')
        #     return super().get_queryset() 
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get('category'):
            try:
                category = self.request.GET.get('category')
                if category == 'all':                
                    context["category"] = Category.objects.filter(actif=True)
                else:                
                    context["category"] = Category.objects.get(id = category)
            except:
                pass
        # context["tags"] = Tag.objects.all()
        context["brands"] = Brand.objects.filter(actif=True)
        gammes = Gamme.objects.filter(actif=True).exclude(name=F('brand__name'))
        context["gammes"] = gammes
        context["filters"] = ProductFilter(self.request.GET, queryset= self.get_queryset())
        # context["products"] = Product.objects.all()
        return context


def filtred_htmx_products(request):
    context = {}
    # print('request', request.GET)
    products = ProductFilter(request.GET, queryset= Product.objects.all())
    context['products'] = products.qs[:24]
    print('context[products]', context['products'])
    return render(request, 'snippets/htmx_products.html', context)

# def sorted_htmx_products(request):
#     context = {}
#     params= request.GET.get('order_by','')
#     print('request.GET', request.GET)
#     print('request params', request.GET.get('order_by'))
#     print('requestccccc', params)
#     if params == "name_a":
#         querySet = Product.objects.all().order_by('name')
#     elif params == "name_z":
#         querySet = Product.objects.all().order_by('-name')
#     elif params == "price":
#         querySet = Product.objects.all().order_by('price')
#     elif params == "brand":
#         querySet = Product.objects.all().order_by('gamme_brand')
#     else:
#         print('je sui laaa')
#         querySet = Product.objects.all()
#     products = ProductFilter(request.GET, queryset=querySet )
#     print('sorted products', products.qs)
#     context['products'] = products.qs
#     return render(request, 'snippets/htmx_products.html', context)
    # return HttpResponse('hello')

def sorted_htmx_products(request):
    context = {}
    print('request.GET', request.GET)
    print('request params', request.GET.get('order_by'))

    querySet = Product.objects.all()
    products = ProductFilter(request.GET, queryset=querySet )
    print('sorted products', products.qs)
    context['products'] = products.qs
    # return render(request, 'snippets/htmx_products.html', 0context)
    return HttpResponse('hello')



class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = "product-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["related"] = Product.objects.filter(actif=True).order_by('?')[:4] 
        context["wilayas"] = Wilaya.objects.all().order_by('name') 
        prod = self.get_object()
        category = prod.category
        products =  Product.objects.filter(category = category)
        context["related_products"] = products.exclude(id= prod.id).order_by('?')[:8]
        context["related_products_count"] = products.count() - 1
        context['form'] = CartAddProductForm()
        # context['atributes'] = prod.product_type.atributes.all()
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


# def set_if_not_none(mapping, key, value):
#     if value is not None:
#         mapping[key] = value