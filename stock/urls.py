from django.urls import path
from .views import ProfileRetrieveView, StockListView, StockView, OperationListView


urlpatterns = [
    path("stocklist/", StockListView.as_view(), name="stock_list"),
    path("stocklist/<str:symbol>/", StockView.as_view(), name="stock_info"),
    path(
        "profile/history/",
        OperationListView.as_view(),
        name="profile_history",
    ),
    path("profile/<str:username>/", ProfileRetrieveView.as_view(), name="profile"),
]
