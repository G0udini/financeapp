from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from .models import Profile, Stock
from .serializers import ProfileSerializer, StockSerializer


class StockListView(ListAPIView):
    serializer_class = StockSerializer
    queryset = Stock.objects.all()


class ProfileRetrieveView(RetrieveAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.select_related("user")

    def get_object(self):
        username = self.kwargs.get("username")
        return self.queryset.get(user__username=username)
