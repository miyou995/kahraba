from django.urls import path
from .views import PartnerListView, RealisationListView

app_name = 'business'

urlpatterns = [
   path('partenaires', PartnerListView.as_view(), name='partner'),
   path('projets', RealisationListView.as_view(), name='realisation'),
   # path('checkout', CheckoutView.as_view(), name='CheckoutView'),
]

