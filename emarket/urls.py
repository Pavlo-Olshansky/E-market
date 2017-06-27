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

admin.autodiscover()

urlpatterns = [

	# Admin URL
    url(r'^admin/', admin.site.urls),

    # Home page
    url(r'^', include('home.urls', namespace='home'), name='home'),

    # Sign up
    url(r'^signup/', include('userprofile.urls', namespace='userprofile'), name='userprofile'),

    # url(r'^signup/$', core_views.signup, name='signup'),

    # Login/Logout URLs
    url(r'^login/$', auth_views.login, {'template_name': 'registration/login.html'}, name='login'),

    url(r'^logout/$', auth_views.logout, {'template_name': 'registration/logout.html','next_page': '/'}, name='logout'),

    # Reset password
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    
    # Social login

    # User profile related URLs

    # Seller related URLs

    # Contact us related URLS




] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
