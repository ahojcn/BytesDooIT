from django.urls import path
from apps.util.views import CSRFTokenView

urlpatterns = [
    path('get_csrf_token/', CSRFTokenView.as_view()),
]
