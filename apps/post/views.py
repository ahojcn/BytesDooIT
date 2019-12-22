import datetime

from django.conf import settings
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response

from post.models import Post


class PostView(APIView):

    def get(self, request):
        """
        获取最新文章，分页
        """
        resp_data = {'status_code': 0, 'msg': '成功', 'data': {}}

        # from user.models import User
        # import random
        # u = User.objects.get(username='ahojcn0')
        # Post.objects.create(user=u, title=str(random.randrange(0, 100000)), content='123')

        # 当前页
        page_index = int(request.query_params.get('page_index', 1))
        # 每页大小
        page_size = int(request.query_params.get('page_size', 10))

        posts = Post.objects.filter(is_delete=False, is_draft=False).order_by('update_datetime')
        total_post = len(posts)
        paged_posts = Paginator(posts, page_size)

        posts = paged_posts.get_page(page_index)
        total_page = paged_posts.num_pages

        resp_data['data'] = {
            'page_index': page_index,
            'page_size': page_size,
            'total_page': total_page,
            'total_post': total_post,
            'posts': []
        }

        for p in posts:
            tmp = {
                'post_id': p.id,
                'username': p.user.username,
                'title': p.title,
                'content': p.content,
                'create_datetime': p.create_datetime,
                'update_datetime': p.update_datetime,
                'like_count': p.like_count,
                'food_count': p.food_count,
                'extra_data': p.extra_data,
            }
            resp_data['data']['posts'].append(tmp)

        return Response(resp_data)
