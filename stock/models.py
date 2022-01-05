from django.db import models
from django.contrib.auth.models import User


ACTIONS = [
    ("BUY", "buy"),
    ("SEL", "sell"),
]


class Stock(models.Model):
    symbol = models.CharField(max_length=20, db_index=True)
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    ipo = models.DateField()

    def __str__(self) -> str:
        return f"{self.symbol}-{self.name}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=10000)

    def __str__(self) -> str:
        return f"{self.user}"


class Portfolio(models.Model):
    stock = models.OneToOneField(Stock, on_delete=models.PROTECT)
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="portfolios"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    avg_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.stock}"


class Operation(models.Model):

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="operation_history"
    )
    action = models.CharField(max_length=3, choices=ACTIONS)
    share = models.ForeignKey(Stock, on_delete=models.DO_NOTHING)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self) -> str:
        return f"{self.action}-{self.date}"
