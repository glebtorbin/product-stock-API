from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView

from goods.models import (Product, ProductQuantity, Reserve, Stock,
                          StockProductReserve)

from .serializers import ProductSerializer, StockSerializer


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
        if not stock.avail_sign:
            stock.avail_sign = True
            stock.save()
        else:
            stock.avail_sign = False
            stock.save()
        return Response(
            {f"{stock.title} availability status": stock.avail_sign}
        )


class StockBalance(APIView):

    def get(self, request, id):
        prod = {}
        stock = Stock.objects.get(id=id)
        qua = stock.quantity.all()
        total = 0
        for pr in qua:
            prod[pr.product.title] = {
                'code': pr.product.code,
                'quantity': pr.quantity
            }
            total += pr.quantity
        prod['total'] = total
        if total == 0:
            return Response({stock.title: 'Stock is empty'})
        return Response({
            stock.title: prod
        })


class ReserveProduct(APIView):

    def post(self, request, id):
        stock = Stock.objects.get(id=id)
        if not stock.avail_sign:
            return Response(f'Stock {stock.id} is not available')
        products = request.data['reserve']
        reserve = Reserve.objects.create(
            count_positions=0
        )
        reserve.save()
        reserved = []
        unknown_prod = []
        not_in_stock = []
        for pr in products:
            if Product.objects.filter(code=pr).exists():
                pr_id = Product.objects.get(code=pr).id
                if stock.products.filter(id=pr_id).exists():
                    pos = ProductQuantity.objects.get(
                        product=Product.objects.get(code=pr),
                        stock=stock
                    )
                    pos.quantity = pos.quantity - 1
                    pos.save()
                    StockProductReserve.objects.create(
                        reserve=reserve,
                        product=Product.objects.get(code=pr),
                        stock=stock
                    ).save()
                    reserved.append(pr)
                else:
                    not_in_stock.append(pr)
            else:
                unknown_prod.append(pr)
        reserve.count_positions = len(reserved)
        reserve.save()
        return Response({
            'reserve': reserve.id,
            'reserved_positions': reserved,
            'not_available': not_in_stock,
            'unknown_items': unknown_prod
        })


class DeleteReserve(APIView):

    def delete(self, request, id):
        reserve = Reserve.objects.get(id=id)
        reserved_pos = StockProductReserve.objects.filter(
            reserve=reserve
        )
        for pos in reserved_pos:
            qua = ProductQuantity.objects.get(
                product=pos.product,
                stock=pos.stock
            )
            qua.quantity += 1
            qua.save()
        reserved_pos.delete()
        reserve.delete()
        return Response('OK')


class ProductViewSet(CreateModelMixin, ListModelMixin,
                     viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
