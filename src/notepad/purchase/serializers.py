from rest_framework import serializers

from notepad.models import Purchase, PurchaseItem


class PurchaseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseItem
        fields = '__all__'


class PurchaseSerializer(serializers.ModelSerializer):
    purchase_items = PurchaseItemSerializer(many=True, read_only=True)

    class Meta:
        model = Purchase
        fields = '__all__'




