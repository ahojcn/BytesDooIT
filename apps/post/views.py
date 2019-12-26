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
        # todo 获取单个分类信息
        resp_data = {'status_code': 0, 'msg': '成功', 'data': []}

        user_id = request.query_params.get('user_id')

        if user_id is None:
            resp_data['status_code'] = -1
            resp_data['msg'] = '参数不足'
            return Response(resp_data)

        user_obj = User.objects.get(id=user_id)

        # 去重
        pc_name_l = PostCategory.objects.filter(user_id=user_obj, is_delete=False).values('name').distinct()
        pcl = []
        for i in pc_name_l:
            pcl.append(PostCategory.objects.filter(name=i.get('name')).first())

        # pcl = PostCategory.objects.filter(user_id=user_obj, is_delete=False)

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


class PostFoodView(APIView):

    @need_login
    def post(self, request):
        """
        投喂文章辣条
        """
        resp_data = {'status_code': 0, 'msg': '成功', 'data': {}}

        from_username = request.session.get('username')
        post_id = request.data.get('post_id')

        if not all([post_id, from_username]):
            resp_data['status_code'] = -1
            resp_data['msg'] = '参数不足'
            return Response(resp_data)

        from_user = User.objects.get(username=from_username)
        post_obj = Post.objects.get(id=post_id)

        # 拒绝自己给自己投喂
        if from_user.username == post_obj.user.username:
            resp_data['status_code'] = -1
            resp_data['msg'] = '不能给自己投喂哟'
            return Response(resp_data)

        if from_user.food_num == 0:
            resp_data['status_code'] = -1
            resp_data['msg'] = '你没有辣条啦'
            return Response(resp_data)

        # 投喂者辣条减少
        from_user.food_num -= 1
        from_user.save()
        # 文章辣条数增加
        post_obj.food_count += 1
        post_obj.save()
        # 用户辣条数增加
        post_obj.user.food_num += 1
        post_obj.user.save()

        return Response(resp_data)


class PostLikeView(APIView):

    @need_login
    def post(self, request):
        """
        给文章点赞
        """
        resp_data = {'status_code': 0, 'msg': '成功', 'data': {}}

        from_username = request.session.get('username')
        post_id = request.data.get('post_id')

        if not all([post_id, from_username]):
            resp_data['status_code'] = -1
            resp_data['msg'] = '参数不足'
            return Response(resp_data)

        from_user = User.objects.get(username=from_username)
        post_obj = Post.objects.get(id=post_id)

        # 拒绝自己给自己投喂
        if from_user.username == post_obj.user.username:
            resp_data['status_code'] = -1
            resp_data['msg'] = '不能给自己点赞哟'
            return Response(resp_data)

        # 文章辣条数增加
        post_obj.like_count += 1
        post_obj.save()

        return Response(resp_data)


class PostView(APIView):

    def get(self, request):
        """
        有 id 参数
            获取单个文章信息
        否则
            分页获取所有文章

        文章信息带作者信息
        """
        resp_data = {'status_code': 0, 'msg': '成功', 'data': {}}

        # 当前页
        page_index = int(request.query_params.get('page_index', 1))
        # 每页大小
        page_size = int(request.query_params.get('page_size', 10))

        post_id = request.query_params.get('post_id')
        if post_id is not None:
            posts = Post.objects.filter(id=post_id, is_delete=False, is_draft=False)
        else:
            posts = Post.objects.filter(is_delete=False, is_draft=False).order_by('-create_datetime')

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
            # 获取分类信息
            pc = PostCategory.objects.filter(post_id=p.id)
            pcl = []
            for i in pc:
                pcl.append({
                    'id': i.id,
                    'name': i.name,
                    'create_datetime': i.create_datetime,
                    'extra_data': i.extra_data
                })
            # 获取标签信息
            pt = PostTag.objects.filter(post_id=p.id)
            ptl = []
            for i in pt:
                ptl.append({
                    'id': i.id,
                    'name': i.name,
                    'create_datetime': i.create_datetime,
                    'extra_data': i.extra_data
                })
            resp_data['data']['posts'].append({
                'post_id': p.id,
                'user_data': {
                    'username': p.user.username,
                    'email': p.user.email,
                    'desc': p.user.description,
                    'reg_time': p.user.reg_datetime,
                    'avatar': p.user.avatar_path,
                    'level': p.user.level,
                    'exp_val': p.user.exp_val,
                    'food_num': p.user.food_num,
                    'extra_data': p.user.extra_data
                },
                'title': p.title,
                'content': p.content,
                'create_datetime': p.create_datetime,
                'update_datetime': p.update_datetime,
                'like_count': p.like_count,
                'food_count': p.food_count,
                'extra_data': p.extra_data,
                'category': pcl,
                'tags': ptl
            })

        return Response(resp_data)

    @need_login
    def post(self, request):
        """
        新增文章
        """
        username = request.session.get('username')

        resp_data = {'status_code': 0, 'msg': '成功', 'data': {}}

        title = request.data.get('title')
        content = request.data.get('content')
        tags = request.data.get('tags')
        category = request.data.get('category')
        is_draft = request.data.get('is_draft')

        # 参数校验
        if not all([title, content]) or is_draft is None:
            resp_data['status_code'] = -1
            resp_data['msg'] = '写一点什么吧'
            return Response(resp_data)

        # 获取用户对象
        user_obj = User.objects.get(username=username)

        # 保存为草稿
        if is_draft is True:
            # 获取文章 id
            post_id = request.data.get('post_id')
            if post_id is None:
                # 新建文章
                post_obj = Post.objects.create(
                    user=user_obj,
                    title=title,
                    content=content,
                    is_draft=True
                )
            else:
                post_obj = Post.objects.get(id=post_id)
                post_obj.title = title
                post_obj.content = content
                post_obj.save()
            resp_data['status_code'] = 0
            resp_data['msg'] = '保存成功'
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
                'extra_data': post_obj.extra_data,
            }
            return Response(resp_data)

        # 新建文章 post
        post_obj = Post.objects.create(user=user_obj, title=title, content=content, is_draft=is_draft)

        t_data = []
        # 添加 tag
        for t in tags:
            tmp = PostTag.objects.create(user_id=user_obj, post_id=post_obj, name=t)
            t_data.append({
                'tag_id': tmp.id,
                'name': tmp.name,
                'create_datetime': tmp.create_datetime,
                'extra_data': tmp.extra_data
            })
        c_data = []
        # 添加 category
        for c in category:
            tmp = PostCategory.objects.create(user_id=user_obj, post_id=post_obj, name=c)
            c_data.append({
                'category_id': tmp.id,
                'name': tmp.name,
                'create_datetime': tmp.create_datetime,
                'extra_data': tmp.extra_data
            })

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
            'extra_data': post_obj.extra_data,
            'tags': t_data,
            'category': c_data
        }

        return Response(resp_data)
