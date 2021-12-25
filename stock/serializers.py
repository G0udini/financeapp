from django.contrib.auth.models import User
from django.db.models import fields
from rest_framework import serializers
from .models import Operation, Portfolio, Profile, Stock


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ("username",)


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = "__all__"


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
