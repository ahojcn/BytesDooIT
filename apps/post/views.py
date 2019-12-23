import datetime

from django.conf import settings
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response

from post.models import Post, PostCategory, PostTag
from user.models import User
from mauth.glob import need_login


class PostCategoryView(APIView):

    def get(self, request):
        """
        获取用户的文章分类
        """
        resp_data = {'status_code': 0, 'msg': '成功', 'data': []}

        user_id = request.query_params.get('user_id')

        if user_id is None:
            resp_data['status_code'] = -1
            resp_data['msg'] = '参数不足'
            return Response(resp_data)

        user_obj = User.objects.get(id=user_id)
        pcl = PostCategory.objects.filter(user_id=user_obj, is_delete=False)

        for pc in pcl:
            tmp = {
                'category_id': pc.id,
                'user_id': user_obj.id,
                'post_id': pc.post_id.id,
                'category_name': pc.name,
                'create_datetime': pc.create_datetime,
                'extra_data': pc.extra_data
            }
            resp_data['data'].append(tmp)

        return Response(resp_data)


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

        posts = Post.objects.filter(is_delete=False, is_draft=False).order_by('-update_datetime')
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

    @need_login
    def post(self, request):
        """
        新增文章
        """
        username = request.session.get('username')

        resp_data = {'status_code': 0, 'msg': '发布成功', 'data': {}}

        title = request.data.get('title')
        content = request.data.get('content')
        is_draft = request.data.get('is_draft')

        if not all([title, content, not is_draft]):
            resp_data['status_code'] = -1
            resp_data['msg'] = '参数不足'
            return Response(resp_data)

        user_obj = User.objects.get(username=username)

        post_obj = Post.objects.create(user=user_obj, title=title, content=content, is_draft=is_draft)

        resp_data['data'] = {
            'username': post_obj.user.username,
            'post_id': post_obj.id,
            'title': post_obj.title,
            'content': post_obj.content,
            'create_datetime': post_obj.create_datetime,
            'update_datetime': post_obj.update_datetime,
            'like_count': post_obj.like_count,
            'is_draft': post_obj.is_draft,
            'food_count': post_obj.food_count,
            'extra_data': post_obj.extra_data
        }

        return Response(resp_data)
