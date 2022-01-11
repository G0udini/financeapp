from decimal import Decimal
from celery.app import shared_task
from django.core.mail import send_mail
from .models import Stock, Portfolio
from .services import FinnHub

TWOPLACES = Decimal("0.01")
finn_client = FinnHub()


def form_mail(stock, perc):
    if perc < 0:
        subject = "Time to BUY"
        message = f"Price of '{stock}' decrease by {perc}% to your avg stock price. It's a great time to buy stocks"
    else:
        subject = "Time to SELL"
        message = f"Price of '{stock}' increase by {perc}% to your avg stock price. It's a great time to sell your portfolio stocks"
    return subject, message


@shared_task
def price_check():
    stocks = Stock.objects.all()
    for stock in stocks:
        price = Decimal(finn_client.get_current_stock_price(stock.symbol)["price"])
        portfolios = (
            Portfolio.objects.filter(stock=stock)
            .select_related("profile")
            .select_related("profile__user")
        )
        for portfolio in portfolios:
            email = portfolio.profile.user.email
            if email:
                diff = Decimal((price - portfolio.avg_price) / price * 100).quantize(
                    TWOPLACES
                )
                if diff > 10 or diff < -10:
                    subject, message = form_mail(stock, diff)
                    send_mail(subject, message, "admin@finance.com", [email])
