from rest_framework.response import Response


def need_verify_code(func):
    """
    需要验证码 fbv 接口的装饰器
    """

    def wrapper(*args, **kwargs):
        resp_data = {'status_code': 0, 'msg': '成功', 'data': {}}

        request = args[1]
        verify_code = request.data.get('verify_code')
        if verify_code is None:
            resp_data['status_code'] = -1
            resp_data['msg'] = '验证码无效'
            return Response(resp_data)
        if verify_code.upper() != request.session.get('verify_code', default='').upper():
            resp_data['status_code'] = -1
            resp_data['msg'] = '验证码错误'
            return Response(resp_data)

        else:
            return func(*args, **kwargs)

    return wrapper


def need_login(func):
    """
    需要登录 fbv 接口装饰器
    """

    def wrapper(*args, **kwargs):
        request = args[1]

        username = request.session.get('username')

        resp_data = {'status_code': 0, 'msg': '成功', 'data': {}}

        if username is None:
            resp_data['status_code'] = 0
            resp_data['msg'] = '未登录'
            resp_data['data'] = {
                'is_login': False
            }
            return Response(resp_data)
        else:
            return func(*args, **kwargs)

    return wrapper
