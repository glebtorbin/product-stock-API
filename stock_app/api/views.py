from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.mixins import CreateModelMixin, ListModelMixin

from goods.models import Stock, Product
from .serializers import StockSerializer, ProductSerializer


class StockViewSet(CreateModelMixin, ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


class StockAvailSign(APIView):

    def get(self, request, id):
        stock = Stock.objects.get(id=id)
        return Response({"status": stock.avail_sign})


    def post(self, request, id):
        stock = Stock.objects.get(id=id)
        if stock.avail_sign == False:
            stock.avail_sign = True
            stock.save()
        else:
            stock.avail_sign = False
            stock.save()
        return Response({f"{stock.title} availability status": stock.avail_sign})


class StockBalance(APIView):

    def get(self, request, id):
        prod = {}
        stock = Stock.objects.get(id=id)
        products = stock.products.all()
        total = 0
        for pr in products:
            prod[pr.title] = {
                'code': pr.code,
                'quantity': pr.quantity
            }
            total+=pr.quantity
        prod['total'] = total
        if total == 0:
            return Response({stock.title: 'Stock is empty'})
        return Response({
            stock.title: prod
        })




class ProductViewSet(CreateModelMixin, ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

