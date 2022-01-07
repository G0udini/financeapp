from rest_framework.pagination import PageNumberPagination


class OperationPagination(PageNumberPagination):
    page_size = 10
