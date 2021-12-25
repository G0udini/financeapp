from django.urls import path
from .views import ProfileRetrieveView, StockListView


urlpatterns = [
    path("stocklist/", StockListView.as_view(), name="stock_list"),
    path("profile/<str:username>/", ProfileRetrieveView.as_view(), name="profile"),
]
