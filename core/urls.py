from django.urls import path
from core.views import product_details

urlpatterns = [
    path('<int:product_id>', product_details, name='product_details'),
]