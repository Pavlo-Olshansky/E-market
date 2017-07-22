"""emarket URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
# from mysite.core import views as core_views
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.views.generic import TemplateView


admin.autodiscover()

urlpatterns = [

	# Admin URL
    url(r'^admin/', admin.site.urls),

    # Home page
    url(r'^', include('home.urls', namespace='home'), name='home'),
    
    # User profile related URLs
    url(r'^accounts/', include('accounts.urls', namespace='accounts'), name='accounts'),
    
    # Paypal payments
    url(r'^paypal/', include('paypal.standard.ipn.urls')),

    # Social login

    # Seller accounts related URLs
    url(r'^products/', include('products.urls', namespace='products'), name='products'),

    # Contact us related URLS

    # Our team url
    url(r'^our_team/', TemplateView.as_view(template_name='our_team.html'), name='our_team'),



] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
