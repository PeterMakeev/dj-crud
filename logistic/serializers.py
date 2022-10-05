from rest_framework import serializers
from logistic.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']

    def create(self, validated_data):
        positions = validated_data.pop('positions')
        stock = super().create(validated_data)
        for pos in positions:
            stock_product = StockProduct(quantity=pos['quantity'],
                                         price=pos['price'],
                                         product=pos['product'],
                                         stock=stock)
            stock_product.save()
        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')
        stock = super().update(instance, validated_data)
        for pos in positions:
            StockProduct.objects.update_or_create(defaults={'quantity': pos['quantity'],
                                                            'price': pos['price']},
                                                  product=pos['product'],
                                                  stock=stock)

        return stock
