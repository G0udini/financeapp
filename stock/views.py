from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.db import transaction
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from stock.paginations import OperationPagination
from .models import Operation, Portfolio, Profile, Stock
from .serializers import (
    OperationSerializer,
    OperationPostSerializer,
    ProfileSerializer,
    StockSerializer,
    StockListSerializer,
)
from .services import FinnHub, get_stock
from .paginations import OperationPagination
import redis
from decimal import Decimal

TWOPLACES = Decimal("0.01")

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
    def get_queryset(self, symbol: str, method: str):
        try:
            stock = Stock.objects.get(symbol=symbol)
        except ObjectDoesNotExist:
            company = finn_client.get_company_info(symbol)
            if company:
                stock = Stock.objects.create(**company)
            else:
                return None, None, None, None
        quote = get_stock(r, finn_client, symbol)
        if method == "POST":
            profile = Profile.objects.get(user=self.request.user)
            try:
                portfolio = Portfolio.objects.get(profile=profile, stock=stock)
            except ObjectDoesNotExist:
                portfolio = None
            return stock, quote, profile, portfolio
        return stock, quote

    def post_sell(self, serializer, profile, portfolio, total, context):
        serializer_quantity = serializer.validated_data["quantity"]
        if not portfolio:
            return Response(
                data={"data": "You don't have stock in profile"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if portfolio.quantity < serializer_quantity:
            return Response(
                data={"data": "Not enough quantity"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if portfolio.quantity == serializer_quantity:
            portfolio.delete()
        else:
            portfolio.quantity -= serializer_quantity
            portfolio.amount -= serializer_quantity * portfolio.avg_price
            portfolio.save()

        profile.balance += total
        profile.save()
        serializer.save(total=total, share=context["share"], user=context["user"])

    def post_buy(self, serializer, profile, portfolio, total, context):
        if profile.balance < total:
            return Response(
                data={"data": "Not enough balance"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not portfolio:
            portfolio = Portfolio(profile=profile, stock=context["share"])
        portfolio.quantity += serializer.validated_data["quantity"]
        portfolio.amount += total
        portfolio.avg_price = Decimal(portfolio.amount / portfolio.quantity).quantize(
            TWOPLACES
        )
        portfolio.save()

        profile.balance -= total
        profile.save()
        serializer.save(total=total, share=context["share"], user=context["user"])

    def get(self, request, symbol):
        query_obj, quote, *_ = self.get_queryset(symbol, "GET")
        if query_obj and quote:
            serializer = StockSerializer(query_obj, context=quote)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(
            data={"data": "Company is not supported"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def post(self, request, symbol):
        query_obj, price, profile, portfolio = self.get_queryset(symbol, "POST")
        if not price:
            return Response(
                data={"data": "Price is not supported"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        request.data["price"] = Decimal(price["price"]).quantize(TWOPLACES)
        serializer = OperationPostSerializer(data=request.data)

        if serializer.is_valid():
            total = (
                serializer.validated_data["price"]
                * serializer.validated_data["quantity"]
            )
            context = {
                "user": request.user,
                "share": query_obj,
            }

            with transaction.atomic():
                if serializer.validated_data["action"] == "SEL":
                    response = self.post_sell(
                        serializer, profile, portfolio, total, context
                    )
                if serializer.validated_data["action"] == "BUY":
                    response = self.post_buy(
                        serializer, profile, portfolio, total, context
                    )
            if response:
                return response

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)


class ProfileRetrieveView(RetrieveAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.select_related("user").prefetch_related(
        "portfolios", "portfolios__stock"
    )

    def get_object(self):
        user = self.request.user
        queryset = self.get_queryset()
        return get_object_or_404(queryset, user=user)


class OperationListView(ListAPIView):
    serializer_class = OperationSerializer
    pagination_class = OperationPagination

    def get_queryset(self):
        user = self.request.user
        return Operation.objects.select_related("share").filter(user=user)
