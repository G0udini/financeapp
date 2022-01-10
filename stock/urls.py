from django.urls import path
from .views import ProfileRetrieveView, StockListView, StockView, OperationListView, StockHistoryView


urlpatterns = [
    path("stocklist/", StockListView.as_view(), name="stock_list"),
    path("stocklist/<str:symbol>/", StockView.as_view(), name="stock_info"),
    path("stocklist/<str:symbol>/history/", StockHistoryView.as_view(), name="stock_history"),
    path(
        "profile/history/",
        OperationListView.as_view(),
        name="profile_history",
    ),
    path("profile/", ProfileRetrieveView.as_view(), name="profile"),
]
