from django.conf.urls import url
from django.urls import path

from .views import RegistrationAPIView

app_name = 'authentication'

urlpatterns = [
    url(r'users/?$', RegistrationAPIView.as_view(), name="activation")
]
