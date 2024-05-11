from django.urls import path
from .views import index

app_name = "verification"

urlpatterns = [
    path("verify/", index, name="verify")
]


