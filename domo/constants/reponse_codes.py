from enum import Enum


class ResponseCode(Enum):
    OK = (0, 'ok')
    PARAM_MISSING = (1, '参数缺失')
    PARAM_ERROR = (2, '参数错误')
    SERVER_EXCEPTION = (3, '服务器异常')

    PERMISSION_DENIED = (1000, '权限不足')
    USERNAME_OR_PASSWORD_MISSING = (1001, '用户名或密码缺失')
    USERNAME_OR_PASSWORD_ERROR = (1002, '用户名或密码错误')
    LOGIN_EXPIRED = (1003, '登录已过期')
    USER_NOT_EXIST = (1004, '用户不存在')
    LOGIN_REQUIRED = (1005, '请登录')

    MUST_BE_IMAGE = (2000, '请传入图片')
    ARTICLE_NOT_EXIST = (2001, '文章不存在')
    MUST_BE_MARKDOWN = (2002, '请传入 MarkDown 文件')
    IMAGE_TOO_LARGE = (2003, '图片过大')

    FILE_NOT_EXIST = (3000, '文件不存在')
    FILE_TOO_LARGE = (3001, '文件过大')

    WALLPAPER_TOO_LARGE = (4000, '壁纸过大')
    WALLPAPER_NOT_EXIST = (4001, '壁纸不存在')

    VIDEO_FILE_CORRUPTED = (5000, '视频文件损坏')
    VIDEO_SAVE_FIELD = (5001, '视频保存失败')
