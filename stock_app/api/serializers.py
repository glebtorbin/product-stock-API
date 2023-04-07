from rest_framework import serializers
from rest_framework.fields import IntegerField, JSONField

from goods.models import Product, Product_attr, ProductQuantity, Reserve, Stock


class ProductSerializer(serializers.ModelSerializer):
    stocks = serializers.PrimaryKeyRelatedField(
        queryset=Stock.objects.all(), many=True
    )
    data = JSONField(write_only=True)
    quantity = IntegerField(write_only=True)

    class Meta:
        fields = (
            'id', 'title', 'data', 'code',
            'quantity', 'date_create', 'stocks'
        )
        model = Product

    def create(self, data):
        if Product.objects.filter(code=data['code']).exists():
            product = Product.objects.get(code=data['code'])
        else:
            product = Product.objects.create(
                title=data['title'],
                code=data['code'],
            )
        for d in data['stocks']:
            product.stocks.add(d.id)
            product.save()
        v_data = data["data"]
        for i in v_data:
            Product_attr.objects.create(
                name=i,
                value=v_data[i],
                prod_id=product
            ).save()
        for stock in data['stocks']:
            qua = ProductQuantity.objects.filter(
                product=product,
                stock=Stock.objects.get(id=stock.id)
            )
            if qua.exists():
                q = ProductQuantity.objects.get(
                    product=product,
                    stock=Stock.objects.get(id=stock.id)
                )
                q.quantity = q.quantity + data['quantity']
                q.save()
            else:
                ProductQuantity.objects.create(
                    product=product,
                    stock=Stock.objects.get(id=stock.id),
                    quantity=data['quantity']
                ).save()
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        data = super().to_representation(instance)
        if request.method == 'GET':
            attr = Product_attr.objects.filter(prod_id=data['id'])
            for at in attr:
                data[at.name] = at.value
        return data


class ReserveSerializer(serializers.ModelSerializer):
    reserve = JSONField(write_only=True)

    class Meta:
        fields = ('reserve', )
        model = Reserve


class StockSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'title', 'avail_sign', 'date_create')
        model = Stock
