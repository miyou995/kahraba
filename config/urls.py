

from django.contrib import admin
from django.urls import path, include
from config import settings
from django.conf.urls.static import static


urlpatterns = [

    path('', include("core.urls")),
    path('', include("business.urls")),
    path('cart/', include("cart.urls")),
    path('orders/', include("order.urls")),
    path('coupons/', include("coupons.urls")),
    path('delivery/', include("delivery.urls")),
    # path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
    # path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    import debug_toolbar
    urlpatterns += path('__debug__/', include(debug_toolbar.urls)),
    urlpatterns += path('admin/', admin.site.urls),
else:
    urlpatterns += path('kahraba-admin/', admin.site.urls),





