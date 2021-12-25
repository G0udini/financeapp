from django.urls import path
from .views import ProfileRetrieveView, StockListView, OperationListView


urlpatterns = [
    path("stocklist/", StockListView.as_view(), name="stock_list"),
    path("profile/<str:username>/", ProfileRetrieveView.as_view(), name="profile"),
    path(
        "profile/<str:username>/history",
        OperationListView.as_view(),
        name="profile_history",
    ),
]
