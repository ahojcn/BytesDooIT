from django.urls import path

from post.views import (
    PostView,
    PostCategoryView,
    PostFoodView,
    PostLikeView,
    PostImageView,
    PostAdminView,
)

urlpatterns = [
    path('', PostView.as_view()),
    path('category/', PostCategoryView.as_view()),
    path('food/', PostFoodView.as_view()),
    path('like/', PostLikeView.as_view()),
    path('img/', PostImageView.as_view()),
    path('draft/', PostAdminView.as_view()),
]
