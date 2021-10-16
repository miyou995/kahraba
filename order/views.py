from core.models import Product
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views.generic import TemplateView
from django.views.decorators.http import require_POST
# Create your views here.
from django.http import HttpResponse
import weasyprint
from .forms import OrderCreateForm, OrderFormWithQuantity
from .models import  OrderItem, Order
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string
from cart.cart import Cart
from coupons.models import Coupon
from delivery.models import Wilaya, Commune
from business.models import Business
from django.core.mail import EmailMessage
import pprint
from io import BytesIO
def order_create_one_product(request,product_id=None):
    form = OrderFormWithQuantity()
    if request.method == 'POST':
        product = Product.objects.get(id=product_id)
        form = OrderFormWithQuantity(request.POST)
        
        coupon = request.session['coupon_id']
        print('le couson utiliser est : ', coupon)
        # coupon.stock -= 1
        # coupon.used += 1
        # coupon.save()
        # print('le FORMULAIRE', form)
        if form.is_valid():
            cd = form.cleaned_data
            quantity=cd['quantity']
            order = form.save()
            print('le formulaire est valid', quantity)
            # print('ORDER ITEM', order.quantity)
            OrderItem.objects.create(order=order,product=product,price=product.price,quantity=quantity)
            # order = Order.objects.get(id=order)

            subject = f'Commande N°: {order.id}'
            message = f'Chére {order.first_name},\n\n' \
                    f'vous avez passer une commande avec succés' \
                    f'votre identifiant de commande est le: {order.id}'

            response = HttpResponse(content_type='application/pdf' )
            response['Content-Disposition' ] = f'filename=order_{order.id}.pdf'
            business   = Business.objects.last().name
            html = render_to_string('order_pdf.html' , {'order' : order, 'business': business})
            pdf_file = weasyprint.HTML(string=html).write_pdf(response)
            mail = EmailMessage(subject, message, 'inter.taki@gmail.com',[order.email])
            mail.attach(pdf_file,out.getvalue(),'application/pdf')
            mail.send()
            return render(request, 'created.html', {'order': order})
            # print('ORDER ITEM')
            # return render(request, 'created.html', {'order': order})
        else:
            # print('yhnooo')
            return redirect(reverse('core:index'))
    return render(request, 'product-detail.html', { 'form' : form})


#  ORDER CREATE

def order_create(request):
    cart = Cart(request)
    wilayas= Wilaya.objects.all().order_by('name') 
    communes= Commune.objects.all().order_by('name') 
    form = OrderCreateForm()
    
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
                    OrderItem.objects.create(order=order,product=item['product'],price=item['price'],quantity=item['quantity'])
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
                    mail = EmailMessage(subject, message, 'inter.taki@gmail.com',[order.email])
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
                return render(request, 'checkout.html', {'cart':cart, 'form' : form, 'wilayas': wilayas, 'communes': communes})
    return render(request, 'checkout.html', {'cart':cart, 'form' : form, 'wilayas': wilayas, 'communes': communes})
    
    

@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_detail.html', {'order': order})

@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    response = HttpResponse(content_type='application/pdf' )
    response['Content-Disposition' ] = f'filename=order_{order.id}.pdf'
    business   = Business.objects.get(id=1).name
    html = render_to_string('order_pdf.html' , {'order' : order, 'business': business})
    # stylesheets=[weasyprint.CSS(str(configs.STATIC_ROOT) + 'css/pdf.css' )]
    weasyprint.HTML(string=html).write_pdf(response)
    return response


# @staff_member_required
# def admin_order_pdf(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
#     html = render_to_string('pdf.html', {'order': order})
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
#     # weasyprint.HTML(string=html).write_pdf(response)
#     # ajouter le style plus t ard erreur ???
#     # weasyprint.HTML(string=html).write_pdf(response)

#     html = render_to_string('pdf.html' , {'order' : order})
#     stylesheets=[weasyprint.CSS(configs.STATIC_ROOT + 'css/pdf.css' )]
#     weasyprint.HTML(string=html).write_pdf(response,stylesheets=stylesheets)

#     return response


















# def order_create(request):
#     cart = Cart(request)
#     wilayas= Wilaya.objects.all().order_by('name') 
#     form = OrderFormWithOutQuantity()
    
#     coupon_id = request.session['coupon_id']
#     if coupon_id:
#         coupon = Coupon.objects.get(id=coupon_id)
#         if cart.__len__() :
#             print('request', request.method)
#             if request.method == 'POST':
#                 form = OrderFormWithOutQuantity(request.POST)
#                 if form.is_valid():
#                     print('le formulaire est valid')
#                     order = form.save(commit=False)
#                     order.delivery_cost = order.wilaya.price
#                     print('delivery cost', order.wilaya.price)
#                     for item in cart:
#                         OrderItem.objects.create(order=order,product=item['product'],price=item['price'],quantity=item['quantity'])
#                     coupon.stock -= 1
#                     coupon.used += 1
#                     coupon.save()
#                     # cart.clear()
#                     return render(request, 'created.html', {'order': order})
#         else: 
#             return redirect(reverse('core:IndexView'))
#     else:
#         if cart.__len__() :
#             print('request', request.method)
#             if request.method == 'POST':
#                 form = OrderFormWithOutQuantity(request.POST)
#                 if form.is_valid():
#                     print('le formulaire est valid')
#                     order = form.save()
#                     for item in cart:
#                         OrderItem.objects.create(order=order,product=item['product'],price=item['price'],quantity=item['quantity'])
#                     cart.clear()
#                     total_price = cart.get_total_price_after_discount()
#                     total_price_with_delivery = total_price + order.delivery_cost

#                     context = {
#                         'order': order,
#                            'products_total': products_total, 
#                            'total_price': total_price,
#                            'delivery': order.delivery,
#                            'total_price_with_delivery': total_price_with_delivery
#                     }
#                     return render(request, 'created.html', context)
#     return render(request, 'create.html', {'cart':cart, 'form' : form, 'wilayas': wilayas})




