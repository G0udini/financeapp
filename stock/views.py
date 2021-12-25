# from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Operation, Profile, Stock
from .serializers import OperationSerializer, ProfileSerializer, StockSerializer


class StockListView(ListAPIView):
    serializer_class = StockSerializer
    queryset = Stock.objects.all()


class ProfileRetrieveView(RetrieveAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.select_related("user").prefetch_related(
        "portfolios", "portfolios__stock"
    )

    def get_object(self):
        queryset = self.get_queryset()
        username = self.kwargs.get("username")
        return get_object_or_404(queryset, user__username=username)


class OperationListView(ListAPIView):
    serializer_class = OperationSerializer

    def get_queryset(self):
        username = self.kwargs.get("username")
        return (
            Operation.objects.select_related("user")
            .select_related("share")
            .filter(user__username=username)
        )
