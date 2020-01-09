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
        resp_data = {'status_code': 0, 'msg': '添加成功', 'data': {}}

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
            except Exception as e:
                resp_data['status_code'] = -1
                resp_data['msg'] = '未知错误' + str(e)
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
            finally:
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
