import logging
from enum import Enum

from rest_framework.renderers import JSONRenderer
from rest_framework import status

from constants.reponse_codes import ResponseCode

logger = logging.getLogger(__name__)


class CustomRenderer(JSONRenderer):
    """
    自定义返回处理
    """
    # 重构 render 方法
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context:
            response = renderer_context['response']
            # 只处理 content_type 为 'application/json' 的响应
            if response.headers['Content-Type'] == self.media_type:
                logger.info('response data: %s', data)
                res_data = {}
                # 只返回了 ResponseCode 枚举类，没有数据
                if isinstance(data, Enum):
                    code, msg = data.value
                # 返回了 ResponseCode 枚举类和数据
                elif isinstance(data, tuple):
                    if isinstance(data[0], Enum):
                        code, msg = data[0].value
                        res_data = data[1]
                    else:
                        code, msg = ResponseCode.OK.value
                        res_data = data
                # 只返回了数据
                else:
                    code, msg = ResponseCode.OK.value
                    res_data = data
                if response.status_code == status.HTTP_401_UNAUTHORIZED:
                    response.status_code = status.HTTP_200_OK
                    code, msg = ResponseCode.LOGIN_REQUIRED.value
                elif response.status_code == status.HTTP_400_BAD_REQUEST:
                    response.status_code = status.HTTP_200_OK
                    code, msg = ResponseCode.PARAM_ERROR.value
                elif response.status_code == status.HTTP_403_FORBIDDEN:
                    response.status_code = status.HTTP_200_OK
                    code, msg = ResponseCode.PERMISSION_DENIED.value
                ret = {'code': code, 'msg': msg, 'data': res_data}
                # 返回 JSON 数据
                return super().render(ret, accepted_media_type, renderer_context)
            else:
                return super().render(data, accepted_media_type, renderer_context)
        else:
            return super().render(data, accepted_media_type, renderer_context)
