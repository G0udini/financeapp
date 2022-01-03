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
from .services import FinnHub, seconds_to_minute_change

import redis


r = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    charset="utf-8",
    decode_responses=True,
)
finn_client = FinnHub()


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


class StockView(APIView):
    def get_queryset(self, symbol):
        try:
            stock = Stock.objects.get(symbol=symbol)
        except ObjectDoesNotExist:
            company = finn_client.get_company_info(symbol)
            stock = Stock.objects.create(**company)
        if stock:
            quote = r.get(f"{stock.symbol}")
            if not quote:
                quote = finn_client.get_current_stock_price(stock.symbol)
                r.set(
                    f"{stock.symbol}",
                    f"{quote['price']}|{quote['change']}",
                    seconds_to_minute_change(),
                )
            else:
                price, change = str(quote).split("|")
                quote = {"price": price, "change": change}
            return stock, quote
        return

    def get(self, request, symbol):

        query_obj, quote = self.get_queryset(symbol)
        serializer = StockSerializer(query_obj, context=quote)
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
