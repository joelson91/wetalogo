from django.shortcuts import render
from core.models import Product


def index(request):
    products = Product.objects.all()
    return render(request, "index.html", {'products': products})


def product_details(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, "product.html", {'product': product})


def checkout(request):
    return render(request, "checkout.html")
