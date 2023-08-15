from .views import nft_list
from django.urls import path
from . import views
from .views import generate_challenge, verify_signature

urlpatterns = [
    path('', views.base,name=""),
    path('generate_challenge/', generate_challenge, name='generate-challenge'),
    path('verify_signature/', verify_signature, name='verify_signature'),
    path('nfts/', nft_list, name='nft-list'),


]
