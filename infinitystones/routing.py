from django.urls import path

from infinitystones.consumer import StoneActivationStatus

urlpatterns = [
    path('wc/stone_activation_status/', StoneActivationStatus.as_asgi()),
]
