import json
import logging

import jwt
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(MiddlewareMixin):
    """
    记录接口请求信息
    """
    def process_request(self, request):
        # 使用 nginx 代理时，request.META.get('REMOTE_ADDR') 获取到的是 nginx 的 ip，需要在 nginx 配置中添加请求头记录客户端 ip
        # 先获取 X-Forwarded-For 中的第一个，然后是 X-Real-IP ，最后 REMOTE_ADDR
        x_forwarded_for = request.headers.get('X-Forwarded-For')
        x_real_ip = request.headers.get('X-Real-IP')
        if x_forwarded_for:
            client_ip = x_forwarded_for.split(',')[0].strip()
        elif x_real_ip:
            client_ip = x_real_ip
        else:
            client_ip = request.META.get('REMOTE_ADDR')
        # 记录 ip 方便在视图中使用
        request.META['CLIENT_IP'] = client_ip
        # 如果需要记录用户信息，并且用户已登录
        logger.info('%s %s from %s', request.path, request.method, client_ip)
        return None


class JsonHandleMiddleware:
    """将请求中的 json 数据反序列化"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 根据 content_type 判断
        if request.content_type == 'application/json':
            try:
                request.json = json.loads(request.body)
            except Exception as e:
                logger.error('请求参数异常：%s %s', e, request.body)
                return 2

        response = self.get_response(request)
        return response


def is_excluded_endpoint(path: str, method: str) -> bool:
    """
    白名单校验
    :param path: 请求路径
    :param method: 请求方式
    :return: 是否在白名单中
    """
    for endpoint in settings.LOGIN_WHITE_LIST:
        if (path == endpoint['path'] or (endpoint['path'].endswith('*') and path.startswith(endpoint['path'].removesuffix('*')))) and (method in endpoint['methods'] or '*' in endpoint['methods']):
            return True
    return False


class JWTMiddleware:
    """jwt 校验"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.info('%s %s', request.path, request.method)
        # 根据 token 获取用户信息
        res_code = 0
        # request.user = None
        authorization_header = request.headers.get('Authorization', '')
        if authorization_header:
            _, token = authorization_header.split(' ')
            try:
                # 根据 jwt 获取 user id 查询出用户信息
                user_id = jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256']).get('user_id')
                user = User.objects.filter(id=user_id).first()
                if user:
                    request.user = user
                else:
                    logger.error('用户不存在：%s', user_id)
                    res_code = 1004
            except jwt.ExpiredSignatureError as _:
                logger.error('token 过期')
                res_code = 1003
            except jwt.InvalidTokenError as _:
                logger.error('不可用的 token')
                res_code = 1003
            except Exception as _:
                logger.error('token 校验失败：%s', _)
                res_code = 1003
        else:
            res_code = 1003

        # 如果接口限制登录，返回错误码
        if not is_excluded_endpoint(request.path, request.method) and res_code != 0:
            return res_code

        response = self.get_response(request)
        return response
