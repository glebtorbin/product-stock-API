from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.fields import CharField, JSONField

from goods.models import Stock, Product, Product_attr


class ProductSerializer(serializers.ModelSerializer):
    stocks = serializers.PrimaryKeyRelatedField(queryset=Stock.objects.all(), many=True)
    data = JSONField(write_only=True)

    class Meta:
        fields = ('id', 'title', 'data', 'code', 'quantity', 'date_create', 'stocks')
        model = Product
    
    def create(self, data):
        product = Product.objects.create(
            title = data['title'],
            code = data['code'],
            quantity = data['quantity'],
        )
        product.stocks.set(data['stocks'])
        product.save()
        v_data = data["data"]
        for i in v_data:
            Product_attr.objects.create(
                name = i,
                value = v_data[i],
                prod_id = product
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


class StockSerializer(serializers.ModelSerializer):
    products = ProductSerializer(read_only=True, many=True)

    class Meta:
        fields = ('id', 'title','avail_sign', 'date_create', 'products')
        model = Stock