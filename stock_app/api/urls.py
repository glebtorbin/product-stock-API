from rest_framework import routers
from django.contrib import admin
from django.urls import path, include
from .views import StockViewSet, StockAvailSign, ProductViewSet, StockBalance, ReserveProduct

router = routers.DefaultRouter()
router.register(r'stocks', StockViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('reserve/<int:id>', ReserveProduct.as_view()),
    path('stock_status/<int:id>', StockAvailSign.as_view()),
    path('stock_balance/<int:id>', StockBalance.as_view()),
]
