from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('predict/', views.predict_crop, name='predict'),
    path('market/', views.market_analysis, name='market'),
]
