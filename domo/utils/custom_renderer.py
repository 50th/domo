import logging

from rest_framework.renderers import JSONRenderer
from rest_framework import status

from constants.reponse_codes import code_msg_map

logger = logging.getLogger(__name__)


class CustomRenderer(JSONRenderer):
    """
    自定义返回处理
    """
    # 重构render方法
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context:
            response = renderer_context['response']
            # 只处理 content_type 为 'application/json' 的响应
            if response.headers['Content-Type'] == self.media_type:
                if isinstance(data, int):
                    # 只返回错误码，没有数据，默认为 {}
                    code = data
                    data = {}
                elif isinstance(data, tuple):
                    # 包括错误码和数据
                    code, data = data
                else:
                    # 只有数据，错误码默认为 0
                    code = 0
                if response.status_code == status.HTTP_401_UNAUTHORIZED:
                    response.status_code = status.HTTP_200_OK
                    code = 1005
                elif response.status_code == status.HTTP_400_BAD_REQUEST:
                    response.status_code = status.HTTP_200_OK
                    code = 2
                elif response.status_code == status.HTTP_403_FORBIDDEN:
                    response.status_code = status.HTTP_200_OK
                    code = 1000
                ret = {'code': code, 'msg': code_msg_map.get(code, ''), 'data': data}
                # 返回 JSON 数据
                return super().render(ret, accepted_media_type, renderer_context)
            else:
                return super().render(data, accepted_media_type, renderer_context)
        else:
            return super().render(data, accepted_media_type, renderer_context)
