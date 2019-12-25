from django.urls import path

from post.views import PostView, PostCategoryView, PostFoodView, PostLikeView

urlpatterns = [
    path('', PostView.as_view()),
    path('category/', PostCategoryView.as_view()),
    path('food/', PostFoodView.as_view()),
    path('like/', PostLikeView.as_view()),
]
