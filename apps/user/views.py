import re
import hashlib
import datetime

from django.conf import settings
from django.shortcuts import render
from itsdangerous import TimedJSONWebSignatureSerializer, SignatureExpired
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import User
from mauth.glob import need_verify_code, need_login
from util.celery_tasks import tasks


class UserView(APIView):

    # todo get 获取单个用户信息

    @need_verify_code
    def post(self, request):
        """
        用户注册
        """
        resp_data = {'data': {}, 'status_code': 0, 'msg': '成功'}
        # print(request.META.get('REMOTE_ADDR'))

        # request.META.get('HTTP_X_FORWARDED_FOR') if request.META.get('HTTP_X_FORWARDED_FOR') else request.META.get(
        # 'REMOTE_ADDR')

        username = request.data.get('username')
        email = request.data.get('email')
        pwd = request.data.get('pwd')
        c_pwd = request.data.get('c_pwd')
        is_agree = request.data.get('is_agree')

        # 数据校验
        if not all([username, email, pwd, c_pwd, is_agree]):
            resp_data['status_code'] = -1
            resp_data['msg'] = '参数不足'
            return Response(resp_data)

        if is_agree is None or bool(is_agree) is False:
            resp_data['status_code'] = -1
            resp_data['msg'] = '请先同意用户协议'
            return Response(resp_data)

        if pwd != c_pwd:
            resp_data['status_code'] = -1
            resp_data['msg'] = '两次输入密码不一致'
            return Response(resp_data)

        if not re.match(r'^[a-zA-Z0-9_-]{4,16}$$', username):
            resp_data['status_code'] = -1
            resp_data['msg'] = '用户名必须是4-16位之间的字母、数字、下划线组成'
            return Response(resp_data)

        if not re.match(r'^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', email):
            resp_data['status_code'] = -1
            resp_data['msg'] = '邮箱格式错误'
            return Response(resp_data)

        # 判断用户是否存在
        if len(User.objects.filter(email=email)) != 0:
            resp_data['status_code'] = -1
            resp_data['msg'] = '该邮箱已被注册'
            return Response(resp_data)
        if len(User.objects.filter(username=username)) != 0:
            resp_data['status_code'] = -1
            resp_data['msg'] = '用户已存在'
            return Response(resp_data)

        # 新增未注册用户
        pwd_md5 = hashlib.md5(pwd.encode('utf-8')).hexdigest()
        try:
            user_obj = User.objects.create(username=username, password=pwd_md5, email=email, is_active=False)
        except Exception as e:
            print(e)
            resp_data['status_code'] = -2
            resp_data['msg'] = '未知错误'
            return Response(resp_data)

        # 生成激活链接
        s = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, 60 * 60 * 24)
        info = {'user_id': user_obj.id}
        token = s.dumps(info).decode('utf8')  # bytes -> utf8

        # 发送激活邮件
        active_url = settings.BASE_WEB_URL + 'api/user/active/?token=' + token
        tasks.send_email.delay('激活你的账号', '', [email], 'email_user_active.html',
                               {'username': username, 'email': email, 'active_url': active_url})

        # 返回用户信息
        resp_data['status_code'] = 0
        resp_data['msg'] = '成功，已发送激活邮件'
        resp_data['data'] = {
            'user_id': user_obj.id,
            'username': user_obj.username,
            'email': user_obj.email,
            'gender': user_obj.gender,
            'description': user_obj.description,
            'reg_datetime': user_obj.reg_datetime,
            'avatar_path': user_obj.avatar_path,
            'last_login_datetime': user_obj.last_login_datetime,
            'level': user_obj.level,
            'exp_val': user_obj.exp_val,
            'food_num': user_obj.food_num,
            'is_mute': user_obj.is_mute,
            'is_active': user_obj.is_active,
            'extra_data': user_obj.extra_data
        }

        # 设置 session 记住登录
        request.session['username'] = user_obj.username

        return Response(resp_data)


class UserActive(APIView):

    @need_login
    def post(self, request):
        """
        重新发送激活邮件
        """
        username = request.session.get('username')
        print(username)
        resp_data = {'status_code': 0, 'msg': '成功', 'data': {}}

        if username is None:
            resp_data['status_code'] = -1
            resp_data['msg'] = '未登录'
            return Response(resp_data)

        user_obj = User.objects.get(username=username)
        # 生成激活链接
        s = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, 60 * 60 * 24)
        info = {'user_id': user_obj.id}
        token = s.dumps(info).decode('utf8')  # bytes -> utf8

        # 发送激活邮件
        active_url = settings.BASE_WEB_URL + 'api/user/active/?token=' + token
        tasks.send_email.delay('激活你的账号', '', [user_obj.email], 'email_user_active.html',
                               {'username': username, 'email': user_obj.email, 'active_url': active_url})

        resp_data['msg'] = '已发送激活邮件，请注意查收'
        return Response(resp_data)

    def get(self, request):
        """
        用户激活
        """
        token = request.query_params.get('token')

        if token is None:
            # token 不存在
            return Response('链接失效', status=404)

        resp_data = {'status_code': 0, 'msg': '成功', 'data': {}}

        s = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, 3600)
        try:
            user_id = s.loads(token)['user_id']
            user_obj = User.objects.get(id=user_id)
            user_obj.is_active = True
            user_obj.save()

            resp_data['status_code'] = 0
            resp_data['msg'] = '成功'
            resp_data['data'] = {
                'user_id': user_obj.id,
                'username': user_obj.username,
                'email': user_obj.email,
                'gender': user_obj.gender,
                'description': user_obj.description,
                'reg_datetime': user_obj.reg_datetime,
                'avatar_path': user_obj.avatar_path,
                'last_login_datetime': user_obj.last_login_datetime,
                'level': user_obj.level,
                'exp_val': user_obj.exp_val,
                'food_num': user_obj.food_num,
                'is_mute': user_obj.is_mute,
                'is_active': user_obj.is_active,
                'extra_data': user_obj.extra_data
            }
        except SignatureExpired:
            # 激活用的 token 过期
            resp_data['status_code'] = -1
            resp_data['msg'] = '链接已过期'
        except Exception as e:
            print(e)
            resp_data['status_code'] = -2
            resp_data['msg'] = '未知错误'
        finally:
            return render(request, 'user_active.html', resp_data)


class UserSession(APIView):

    @need_verify_code
    def post(self, request):
        """
        登录
        """
        username = None
        is_username = request.data.get('is_username')
        pwd = request.data.get('pwd')
        local_time = request.data.get('local_time')

        resp_data = {'status_code': 0, 'msg': '成功', 'data': {}}

        # 参数校验
        if not all([is_username, pwd, local_time]):
            resp_data['status_code'] = -1
            resp_data['msg'] = '参数不足'
            return Response(resp_data)

        is_username = bool(is_username)
        if is_username is True:
            username = request.data.get('username')
            user_obj_set = User.objects.filter(username=username)
        else:
            email = request.data.get('email')
            user_obj_set = User.objects.filter(email=email)

        if len(user_obj_set) == 0:
            resp_data['status_code'] = -1
            resp_data['msg'] = '用户名或邮箱有误'
            return Response(resp_data)

        user_obj = user_obj_set.get(username=username)
        # 校验密码是否匹配
        pwd_md5 = hashlib.md5(pwd.encode('utf-8')).hexdigest()
        if pwd_md5 != user_obj.password:
            resp_data['status_code'] = -1
            resp_data['msg'] = '密码有误'
            return Response(resp_data)

        # 用户名密码正确，记录登录时间
        user_obj.last_login_datetime = datetime.datetime.fromtimestamp(int(local_time))
        user_obj.save()

        # 记住登录状态
        request.session['username'] = user_obj.username

        resp_data['status_code'] = 0
        resp_data['msg'] = '成功'
        resp_data['data'] = {
            'user_id': user_obj.id,
            'username': user_obj.username,
            'email': user_obj.email,
            'gender': user_obj.gender,
            'description': user_obj.description,
            'reg_datetime': user_obj.reg_datetime,
            'avatar_path': user_obj.avatar_path,
            'last_login_datetime': user_obj.last_login_datetime,
            'level': user_obj.level,
            'exp_val': user_obj.exp_val,
            'food_num': user_obj.food_num,
            'is_mute': user_obj.is_mute,
            'is_active': user_obj.is_active,
            'extra_data': user_obj.extra_data
        }

        return Response(resp_data, status=200)

    def get(self, request):
        """
        获取会话信息（判断是否已登录）
        """
        username = request.session.get('username')

        resp_data = {'status_code': 0, 'msg': '成功', 'data': {}}

        if username is None:
            resp_data['status_code'] = 0
            resp_data['msg'] = '未登录'
            resp_data['data'] = {
                'is_login': False
            }
        else:
            user_obj_set = User.objects.filter(username=username)
            if len(user_obj_set) == 0:
                resp_data['status_code'] = -1
                resp_data['msg'] = '未登录'
                resp_data['data'] = {
                    'is_login': False
                }
                return Response(resp_data)

            user_obj = user_obj_set.get(username=username)
            resp_data['status_code'] = 0
            resp_data['msg'] = '已登录'
            resp_data['data'] = {
                'is_login': True,
                'user_id': user_obj.id,
                'username': user_obj.username,
                'email': user_obj.email,
                'gender': user_obj.gender,
                'description': user_obj.description,
                'reg_datetime': user_obj.reg_datetime,
                'avatar_path': user_obj.avatar_path,
                'last_login_datetime': user_obj.last_login_datetime,
                'level': user_obj.level,
                'exp_val': user_obj.exp_val,
                'food_num': user_obj.food_num,
                'is_mute': user_obj.is_mute,
                'is_active': user_obj.is_active,
                'extra_data': user_obj.extra_data
            }

        return Response(resp_data)

    @need_login
    def delete(self, request):
        """
        登出
        """
        # 删除所有 session
        request.session.flush()

        resp_data = {'status_code': 0, 'msg': '成功', 'data': {}}

        return Response(resp_data)
