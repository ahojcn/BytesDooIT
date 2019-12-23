from django.urls import path

from post.views import PostView, PostCategoryView

urlpatterns = [
    path('', PostView.as_view()),
    path('category/', PostCategoryView.as_view()),
]
