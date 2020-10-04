from django.db import models


class Bonds(models.Model):
    isin = models.CharField(max_length=200)
    size = models.IntegerField()
    currency = models.CharField(max_length=200)
    maturity = models.DateField()
    lei = models.CharField(max_length=200)
    legal_name = models.CharField(max_length=200)