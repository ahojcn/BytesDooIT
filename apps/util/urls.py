from django.urls import path
from apps.util.views import CSRFTokenView, VerifyCodeImgView

urlpatterns = [
    path('csrf_token/', CSRFTokenView.as_view()),
    path('verify_code_img/', VerifyCodeImgView.as_view()),
]
