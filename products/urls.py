from django.conf.urls import url
from .views import ProductsPage

urlpatterns = [

    url(r'^$', ProductsPage.as_view(), name='products_page'),

]
