from django.urls import path
from . import views

urlpatterns = [
    path("callback-request", views.callback_request_view, name="callback_request"),
]
