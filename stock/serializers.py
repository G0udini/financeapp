from django.contrib.auth.models import User
from django.db.models import fields
from rest_framework import serializers
from .models import Profile, Stock


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ("username",)

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = "__all__"



class ProfileSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    user = serializers.StringRelatedField()

    class Meta:
        model = Profile
        fields = ("user", "portfolio", "balance")
