from rest_framework.response import Response


def need_verify_code(func):
    """
    需要验证码 fbv 接口的装饰器
    """

    def wrapper(*args, **kwargs):
        resp_data = {'status_code': 0, 'msg': '成功', 'data': {}}

        request = args[1]
        verify_code = request.data.get('verify_code')
        if verify_code.upper() != request.session.get('verify_code', default='').upper():
            resp_data['status_code'] = -1
            resp_data['msg'] = '验证码错误'
            return Response(resp_data)

        else:
            return func(*args, **kwargs)

    return wrapper
