from django.urls import include, path
from rest_framework import routers

from .views import (DeleteReserve, ProductViewSet, ReserveProduct,
                    StockAvailSign, StockBalance, StockViewSet)

router = routers.DefaultRouter()
router.register(r'stocks', StockViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('deleteres/<int:id>', DeleteReserve.as_view()),
    path('reserve/<int:id>', ReserveProduct.as_view()),
    path('stock_status/<int:id>', StockAvailSign.as_view()),
    path('stock_balance/<int:id>', StockBalance.as_view()),
]
