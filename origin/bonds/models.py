"""
    Bond Models with workflow to update models shown below
    - Change your models (in models.py).
    - Run python manage.py makemigrations to create migrations for those changes
    - Run python manage.py migrate to apply those changes to the database.

    Create admin user:
    - python manage.py createsuperuser

    *** Remove in production environment ***
        - User: Rt247
        - Password: strongpassword
    *** Remove in production environment ***
"""

from django.db import models
from django.contrib.auth import get_user_model

class Bond(models.Model):
    isin = models.CharField(max_length=200)
    size = models.IntegerField()
    currency = models.CharField(max_length=200)
    maturity = models.DateField()
    lei = models.CharField(max_length=200)
    legal_name = models.CharField(max_length=200)
    user = models.ForeignKey(get_user_model(), default=1,
                             null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.lei