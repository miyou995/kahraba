from django.urls import path
from .views import  load_communes, delivery_cost 
app_name ='delivery'
urlpatterns = [
   path('load-communes/', load_communes, name='load_communes'),
   path('delivery_cost/', delivery_cost, name='delivery_cost'),
   #  path('vapecity/', views.vapecity, name='vapecity'),
   #  path('contact/', views.ContactView.as_view(), name='ContactView'),
]