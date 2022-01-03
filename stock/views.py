from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Operation, Profile, Stock
from .serializers import (
    OperationSerializer,
    ProfileSerializer,
    StockSerializer,
    StockListSerializer,
)
from .services import FinnHub




class StockListView(APIView):
    def get_queryset(self):
        queryset = Stock.objects.all()
        search_query = self.request.query_params.get("search", None)
        if search_query:
            queryset = finn_client.get_stock_by_search(search_query)
        return queryset

    def get(self, request):
        queryset = self.get_queryset()
        serializer = StockListSerializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


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
