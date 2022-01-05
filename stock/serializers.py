from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Operation, Portfolio, Profile, Stock


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = "__all__"


class StockSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    change = serializers.SerializerMethodField()

    class Meta:
        model = Stock
        fields = "__all__"

    def get_price(self, obj):
        return float(self.context.get("price"))

    def get_change(self, obj):
        return float(self.context.get("change"))


class StockListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ["symbol", "name"]


class PortfolioSerializer(serializers.ModelSerializer):
    stock = serializers.StringRelatedField()

    class Meta:
        model = Portfolio
        fields = ("stock", "quantity", "amount", "temprary_amount")


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    portfolios = PortfolioSerializer(many=True)

    class Meta:
        model = Profile
        fields = ("user", "portfolios", "balance")


class OperationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    share = serializers.StringRelatedField()

    class Meta:
        model = Operation
        fields = "__all__"


class OperationPostSerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    # share = serializers.PrimaryKeyRelatedField(queryset=Stock.objects.all())

    class Meta:
        model = Operation
        fields = ("price", "quantity", "user", "share", "action")

    def validate_price(self, value):
        if value <= 0:
            raise ValidationError("Price must be positive integer.")
        return value

    def validate_quantity(self, value):
        if value <= 0:
            raise ValidationError("Quantity must be positive integer.")
        return value
