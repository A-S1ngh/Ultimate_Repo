# Generated by Django 3.1.2 on 2020-12-23 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_listing_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='creator',
            field=models.CharField(max_length=64, null=True),
        ),
    ]
