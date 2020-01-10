from django.conf import settings
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response

from user.models import User
from post.models import Post
from video.models import Video
from comment.models import Comment
from mauth.glob import need_login


class CommentView(APIView):

    @need_login
    def post(self, request):
        """
        新增评论
        """
        resp_data = {'status_code': 0, 'msg': '成功', 'data': {}}

        username = request.session.get('username')
        user = User.objects.get(username=username)

        post_id = request.data.get('post_id')
        video_id = request.data.get('video_id')
        ref_id = request.data.get('ref_id')
        content = request.data.get('content')

        if not all([post_id, content]) or all([video_id, content]):
            resp_data['status_code'] = -1
            resp_data['msg'] = '参数不足'
            return Response(resp_data)

        post = None
        if post_id:
            try:
                post = Post.objects.get(id=post_id)
            except ObjectDoesNotExist:
                resp_data['status_code'] = -1
                resp_data['msg'] = '无相关文章'
                return Response(resp_data)
            except Exception as e:
                resp_data['status_code'] = -1
                resp_data['msg'] = '未知错误' + str(e)
                return Response(resp_data)
        video = None
        if video_id:
            try:
                video = Video.objects.get(id=video_id)
            except ObjectDoesNotExist:
                resp_data['status_code'] = -1
                resp_data['msg'] = '无相关视频'
            except Exception as e:
                resp_data['status_code'] = -2
                resp_data['msg'] = '未知错误' + str(e)
                return Response(resp_data)
        ref = None
        try:
            ref = Comment.objects.get(ref=ref_id)
        except ObjectDoesNotExist:
            pass
        except Exception as e:
            resp_data['status_code'] = -2
            resp_data['msg'] = '未知错误' + str(e)
            return Response(resp_data)

        try:
            Comment.objects.create(user=user, post=post, video=video, ref=ref, content=content)
        except Exception as e:
            resp_data['status_code'] = -2
            resp_data['msg'] = '未知错误' + str(e)
            return Response(resp_data)

        return Response(resp_data)

    def get(self, request):
        """
        获取评论
        """
        resp_data = {'status_code': 0, 'msg': '成功', 'data': {}}

        post_id = request.query_params.get('post_id')
        video_id = request.query_params.get('video_id')
        page_index = int(request.query_params.get('page_index', 1))
        page_size = int(request.query_params.get('page_size', 5))

        if not post_id and not video_id:
            resp_data['status_code'] = -1
            resp_data['msg'] = '参数不足'
            return Response(resp_data)

        comments = []
        if post_id:
            comments = Comment.objects.filter(post_id=post_id).order_by('-create_datetime').values()
        if video_id:
            comments = Comment.objects.filter(video_id=video_id).order_by('-create_datetime').values()

        total_comments = len(comments)
        paged_comments = Paginator(comments, page_size)

        comments = paged_comments.get_page(page_index)
        total_page = paged_comments.num_pages

        resp_data['data'] = {
            'page_index': page_index,
            'page_size': page_size,
            'total_page': total_page,
            'total_post': total_comments,
            'comments': []
        }

        for c in comments:
            user = User.objects.get(id=c['user_id'])
            resp_data['data']['comments'].append({
                'id': c['id'],
                'content': c['content'],
                'ref_content': c['ref_id'],
                'like_count': c['like_count'],
                'unlike_count': c['unlike_count'],
                'create_datetime': c['create_datetime'],
                'extra_data': c['extra_data'],
                'username': user.username,
                'avatar': settings.BASE_WEB_URL + user.avatar_path,
            })

        return Response(resp_data)

    @need_login
    def delete(self, request):
        """
        删除评论
        """
        resp_data = {'status_code': 0, 'msg': '成功', 'data': {}}

        username = request.session.get('username')
        user = User.objects.get(username=username)

        comment_id = request.query_params.get('id')

        if not comment_id:
            resp_data['status_code'] = -1
            resp_data['msg'] = '参数不足'
            return Response(resp_data)

        comment = None
        try:
            comment = Comment.objects.get(id=comment_id, user=user)
        except ObjectDoesNotExist:
            resp_data['status_code'] = -1
            resp_data['msg'] = '无相关评论'
            return Response(resp_data)
        except Exception as e:
            resp_data['status_code'] = -2
            resp_data['msg'] = '未知错误' + str(e)
            return Response(resp_data)

        comment.is_delete = True
        comment.save()

        return Response(resp_data)


class CommentLike(APIView):

    @need_login
    def post(self, request):
        """
        喜欢 / 不喜欢某个评论
        """
        resp_data = {'status_code': 0, 'msg': '成功', 'data': {}}

        comment_id = request.data.get('id')
        like = request.data.get('like')

        if not all([comment_id]) and like is None:
            resp_data['status_code'] = -1
            resp_data['msg'] = '参数不足'
            return Response(resp_data)

        like = bool(like)

        try:
            comment = Comment.objects.get(id=comment_id)
        except ObjectDoesNotExist:
            resp_data['status_code'] = -1
            resp_data['msg'] = '评论不存在'
            return Response(resp_data)
        except Exception as e:
            resp_data['status_code'] = -2
            resp_data['msg'] = '未知错误' + str(e)
            return Response(resp_data)

        if like:
            comment.like_count += 1
            comment.save()
        else:
            comment.unlike_count += 1
            comment.save()

        return Response(resp_data)
