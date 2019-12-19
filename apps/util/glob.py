def check_verify_code(request, code):
    """
    校验验证码
    :param request: 请求对象
    :param code: 用户输入的验证码
    :return: True 或者 False
    """
    if code.upper() != request.session.get('verify_code', default='').upper():
        return False
    else:
        return True
