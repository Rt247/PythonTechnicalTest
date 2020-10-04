"""
    bonds URL Configuration

"""
from django.urls import path, include
from bonds.views import BondsListView

urlpatterns = [
    path('', BondsListView.as_view(), name="bonds")
]
