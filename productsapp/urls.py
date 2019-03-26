from django.urls import path

from productsapp.views import ProductsView

urlpatterns = [
    path('', ProductsView.as_view(), name='products'),
]
