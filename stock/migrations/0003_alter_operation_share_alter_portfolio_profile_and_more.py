# Generated by Django 4.0 on 2022-01-03 18:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0002_remove_profile_portfolio_portfolio_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operation',
            name='share',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='stock.stock'),
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='portfolios', to='stock.profile'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='symbol',
            field=models.CharField(db_index=True, max_length=20),
        ),
    ]
