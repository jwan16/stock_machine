from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login', auth_views.login, {'template_name': 'core/login.html'}, name='login'),
    # url(r'^', TemplateView.as_view(template_name='index.html')),
    url(r'^', include('stock.urls')),

    # Model
    url(r'^model/', include('model.urls')),

    # filter
    url(r'^filter/', include('filter.urls')),

    # Backtest
    url(r'^backtest/', include('backtest.urls')),

    # Chartviewer
    url(r'^chartviewer/', include('chartviewer.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)