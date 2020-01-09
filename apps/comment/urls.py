from django.urls import path

from comment.views import (
    CommentView,
    CommentLike
)

urlpatterns = [
    path('', CommentView.as_view()),
    path('like/', CommentLike.as_view()),
]
