# Generated by Django 4.0 on 2021-12-25 11:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='portfolio',
        ),
        migrations.AddField(
            model_name='portfolio',
            name='profile',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='stock.profile'),
            preserve_default=False,
        ),
    ]
