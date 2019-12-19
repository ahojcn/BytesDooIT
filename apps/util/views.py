import io
import random

from PIL import Image, ImageDraw, ImageFont

from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response


class CSRFTokenView(APIView):

    # @csrf_exempt
    def post(self, request):
        """
        获取 csrf token
        """
        resp_data = {'status': 0, 'msg': 'success', 'data': {}}
        token = get_token(request)
        resp_obj = Response(resp_data)
        resp_obj.set_cookie('X-CSRFToken', token)
        return resp_obj


class VerifyCodeImgView(APIView):

    def get(self, request):
        """
        获取图片验证码
        """
        width = request.GET.get('width')
        height = request.GET.get('height')

        if not all([width, height]):
            width = 200
            height = 60
        else:
            width = int(width)
            height = int(height)

        bg_color = (random.randrange(20, 100), random.randrange(20, 100), 255)

        # 画布
        im = Image.new('RGB', (width, height), bg_color)
        # 画笔
        draw = ImageDraw.Draw(im)

        # 绘制噪点
        for i in range(0, 500):
            xy = (random.randrange(0, width), random.randrange(0, height))
            fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
            draw.point(xy, fill=fill)

        # 验证码的备选值
        code = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0qwertyuiopasdfghjklzxcvbnm'
        # 随机选取 4 个作为验证码
        rand_str = ''
        for i in range(0, 4):
            rand_str += code[random.randrange(0, len(code))]

        # 构造字体对象
        font = ImageFont.truetype('static/font/LatienneSwaT.ttf', height, encoding='unic')
        # 构造字体颜色
        font_color = (255, random.randrange(0, 255), random.randrange(0, 255))
        # 绘制 4 个字
        draw.text((0, 0), rand_str[0], font=font, fill=font_color)
        draw.text((width / 4, 0), rand_str[1], font=font, fill=font_color)
        draw.text((width / 4 * 2, 0), rand_str[2], font=font, fill=font_color)
        draw.text((width / 4 * 3, 0), rand_str[3], font=font, fill=font_color)

        # 释放画笔
        del draw

        # 存入 session，做验证对比
        request.session['verify_code'] = rand_str

        # 将验证码图片写入内存
        buf = io.BytesIO()
        im.save(buf, 'png')

        # 返回
        return HttpResponse(buf.getvalue(), 'image/png')
