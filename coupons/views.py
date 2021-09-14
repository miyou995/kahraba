from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Coupon
from .forms import CouponApplyForm

# Create your views here.
@require_POST
def coupon_apply(request):
    print('Request non disponible')
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            #iexact : case insensitive exact match, lte: less than or equal, gte: greater than or equal
            coupon = Coupon.objects.get(code__iexact=code, valid_from__lte=now, valid_to__gte=now, active=True)
            if(coupon.stock > 0 ):
                request.session['coupon_id'] = coupon.id
                coupon.stock -= 1
                coupon.used += 1
                coupon.save()
            else:
                print('Coupon non disponible')
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
     
    return redirect('cart:cart_detail')