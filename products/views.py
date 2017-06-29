from django.shortcuts import render
from django.views.generic.base import TemplateView

class ProductsPage(TemplateView):

	template_name = 'products/products_page.html'
