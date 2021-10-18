from decimal import Context
from django.http.response import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views.generic import TemplateView
from django.views.decorators.http import require_POST
from .cart import Cart
from core.models import Product
from delivery.models import Wilaya, Commune
from coupons.models import Coupon
from order.models import  OrderItem, Order
from business.models import Business
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from .forms import CartAddProductForm, CartUpdateProductQuantityForm
from django.template.loader import render_to_string
from django.contrib import messages
from django.core import serializers
from order.forms import OrderCreateForm
from django.core.mail import EmailMessage
from io import BytesIO
import weasyprint
    
# class CheckoutView(TemplateView):
#     template_name = "checkout.html"

def cart_detail(request):
    cart = Cart(request)
    has_attribute = False
    wilayas= Wilaya.objects.all().order_by('name') 
    communes= Commune.objects.all().order_by('name') 
    form = OrderCreateForm()
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'override': True})
        # print('Wach ahda item details', item)
        try:
            if item['attribute_1']: 
                has_attribute = True
        except:
            pass
    # print('baskets details', list(cart))
    if cart.__len__() :
        # print('request', request.method)
        if request.method == 'POST':
            form = OrderCreateForm(request.POST)
            # print(form)
            if form.is_valid():
                order = form.save()
                order.delivery_cost = order.wilaya.price
                order.save()
                # print('delivery cost', order.wilaya.price)
                for item in cart:
                    OrderItem.objects.create(order=order,product=item['product'],price=item['price'],quantity=item['quantity'],attribute_1 = ['attrbute_1'], attribute_2 = ['attrbute_2'], attribute_3 = ['attrbute_3'])
                try:
                    coupon_id = request.session['coupon_id']
                    coupon = Coupon.objects.get(id=coupon_id)
                    coupon.stock -= 1
                    coupon.used += 1
                    request.session['coupon_id'] = None
                    coupon.save()
                except:
                    pass
                cart.clear()
                total_price = cart.get_total_price_after_discount()
                total_price_with_delivery = total_price + order.delivery_cost
            
                subject = f'Commande N°: {order.id}'
                message = f'Chére {order.first_name},\n\n vous avez passer une commande avec succés' f'votre identifiant de commande est le: {order.id}'
                try :
                    response = HttpResponse(content_type='application/pdf' )
                    response['Content-Disposition' ] = f'filename=order_{order.id}.pdf'
                    business   = Business.objects.last().name
                    html = render_to_string('order_pdf.html' , {'order' : order, 'business': business})
                    out = BytesIO()
                    pdf_file = weasyprint.HTML(string=html).write_pdf(response)
                    mail = EmailMessage(subject, message, 'octopus.emailing@gmail.com',[order.email])
                    mail.attach(pdf_file,out.getvalue(),'application/pdf')
                    mail.send()
                    context = {
                        'order': order,
                        # 'products_total': products_total, 
                        'total_price': total_price,
                        'delivery': order.delivery_cost,
                        'total_price_with_delivery': total_price_with_delivery,
                        'pdf_file': pdf_file,
                    }
                    return render(request, 'created.html', context)
                except :
                    print('yaw matebaatch')
                # stylesheets=[weasyprint.CSS(str(configs.STATIC_ROOT) + 'css/pdf.css' )]
            else: 
                print('the form is not valid')
                return render(request, 'cart.html', {'cart':cart, 'form' : form, 'wilayas': wilayas, 'communes': communes})
    context = {
        'cart': cart,
        'has_attribute' : has_attribute,
        'form' : form,
        'wilayas': wilayas,
        'communes': communes
        # 'coupon_apply_form': coupon_apply_form
    }
    return render(request, 'cart.html', context)


def set_if_not_none(mapping, key, value):
    if value is not None:
        mapping[key] = value



@require_POST # 
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        print('cd', cd)
        cart.add(
            product=product,
            quantity=cd['quantity'],
            override_quantity=cd['override'],
            attribute_1 = cd['attribute_1'],
            attribute_2 = cd['attribute_2'],
            attribute_3 = cd['attribute_3']
        )
        return redirect('cart:cart_detail')

def cart_one_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id= product_id)
        # for atribut in atributes:
        #     print('atribut=> ',type(atribut))
        #     values = atribut.values.all()
        #     print('values=> ',values)
    if product:
        attribute_1 = False
        attribute_2 = False
        attribute_3 = False
        quantity = 1
        try:
            if product.product_type:
                if product.product_type.atributes:
                    atributes = product.product_type.atributes.all()
                    try:
                        attribute_1 = atributes[0].values.first().value
                    except:
                        pass
                    try:
                        attribute_2 = atributes[1].values.first().value
                    except:
                        pass
                    try:
                        attribute_3 = atributes[2].values.first().value
                    except:
                        pass
        except:
            pass
    if attribute_3:
    
        cart.add(
            product=product,
            quantity=quantity,
            attribute_1=attribute_1,
            attribute_2=attribute_2,
            attribute_3=attribute_3
        )
    elif attribute_2:
        cart.add(
            product=product,
            quantity=quantity,
            attribute_1 = attribute_1,
            attribute_2 = attribute_2
        )
    elif attribute_1:

        cart.add(
            product=product,
            quantity=quantity,
            attribute_1 = attribute_1,
        )
    else:
        cart.add(
            product=product,
            quantity=quantity,
        )
    items = len(cart)
    context = {
        'total_price': cart.get_total_price(),
        'length' : len(cart),
    }
    return render(request, 'snippets/cart-count.html',context)
    # return HttpResponse(len(cart))
    # pass


# @require_POST
# def cart_update(request):
#     print('envoer')
#     cart = Cart(request)
#     form =CartUpdateProductQuantityForm(request.POST)
#     context = {
#         'cart': cart,
#         'form' : form
#     }
#     if form.is_valid():
#         cd = form.cleaned_data
#         product_id= cd['product_id']
#         quantity=cd['quantity']
#         product = get_object_or_404(Product, id=product_id)
#         print('id ', product_id)
#         print('quantity ', quantity)
#         print('product ', product)
#         cart.update(
#             product = product,
#             quantity=quantity,
#         )
#         print('lha9t')
#         # return redirect('cart:cart_detail')
#         if request.htmx:
#             return render(request, 'snippets/cart-rows.html',  context)
#         # except:
#         #     print('THE form', form)
#     return render(request, 'snippets/cart-rows.html',  context)




@require_POST
def cart_product_update(request, pk):
    cart = Cart(request)
    form =CartUpdateProductQuantityForm(request.POST)
    context = {
        'cart': cart,
        'form' : form
    }
    if form.is_valid():
        cd = form.cleaned_data
        product_id= cd['product_id']
        quantity=cd['quantity']
        product = get_object_or_404(Product, id=product_id)
        print('id ', product_id)
        print('quantity ', quantity)
        print('product ', product)
        cart.update(
            product = product,
            quantity=quantity,
        )
        print('lha9t')
        # return redirect('cart:cart_detail')
        if request.htmx:
            return render(request, 'snippets/cart-row.html',  context)
        # except:
        #     print('THE form', form)
    return render(request, 'snippets/cart-rows.html',  context)


    if request.htmx:
        print('yes htmx')
        return render(request, 'snippets/cart-rows.html',  context)
    return render(request, 'cart.html', {'cart' : cart})

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')




# def cart_add_one_product(request):
#     cart = Cart(request)
#     # product_id = request.POST['product_id']
#     # Get the product that we want to add
#     p_id = request.GET.get('product_id')
#     print('request', p_id)
#     product = get_object_or_404(Product, id=p_id, actif=True)
#     tailles = product.taille.all()
#     colors = product.couleur.all()

#     print('les couleurs', colors)
#     pointures = product.pointure.all()
#     if tailles:
#         taille = tailles[0]
#     color = colors.first()
#     print('les couleurs', color)

#     if pointures:
#         pointure = pointures[0]
#     if product:
#         quantity = 1
#         try:
#             print('pointure',pointure)
#         except:
#             pass
#         try:
#             print('taille', taille)
#         except:
#             pass
#         try:
#             print(color, 'taille, pointure')
#         except:
#             pass
        
        
#         try:
#             cart.add(
#                 product=product,
#                 quantity=quantity,
#                 pointure = pointure,
#                 color = color
#             ) 
#         except:
#             try:
#                 cart.add(
#                     product=product,
#                     quantity=quantity,
#                     taille = taille,
#                     color = color
#                 )
#             except:
#                 cart.add(
#                     product=product,
#                     quantity=quantity,
#                     color = color
#                 )
#     return JsonResponse(serializers.serialize('json', color), safe=True)

    # if tailles:
    #     taille = tailles[0]
    #     cart.add(taille = taille)

    # else:
    #     taille = False
    # if colors:
    #     color = colors[0]
    #     cart.add(color = color)
    # else:
    #     color = False
    # if pointures:
    #     pointure = pointures[0]
    #     cart.add(pointure = pointure)
    # else:
    #     pointure = False

    # else:
        # return redirect('cart:cart_detail')





# @require_POST
# def cart_one_add(request, product_id):
#     cart = Cart(request)
#     product = get_object_or_404(Product, id=product_id)
#     form = CartAddProductQuantityForm(request.POST)
#     print('the Cart ')
#     try:
#         print('the Cart  ffbf')

#         if form.is_valid():
#                 cd = form.cleaned_data
#                 print('cd', cd)
#                 cart.add(
#                     product=product,
#                     quantity=1,
#                 )
#                 print('the Cart two', cart)
#                 return redirect('cart:cart_detail')
#     except:

#         return redirect('/')

