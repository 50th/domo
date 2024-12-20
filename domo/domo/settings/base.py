"""
Django settings for domo project.

Generated by 'django-admin startproject' using Django 4.2.11.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-(=g@15teaveuc156r_1h@!ce^pk$lnur=slf)ts*q023^47lv5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'app_system.apps.AppSystemConfig',
    'app_user.apps.AppUserConfig',
    'app_article.apps.AppArticleConfig',
    'app_file.apps.AppFileConfig',
    'app_video.apps.AppVideoConfig',
    'app_wallpaper.apps.AppWallpaperConfig',
    'rest_framework',
]

MIDDLEWARE = [
    'utils.middlewares.RequestLoggingMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # 加入中间键 位置必须在这里 不能在其他位置
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'domo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'domo.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db' / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_PAGINATION_CLASS': 'utils.custom_pagination.CustomPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_RENDERER_CLASSES': (
        'utils.custom_renderer.CustomRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        # 限制次数，未登录用户一分钟最多三次，登录用户最多一分钟十次
        'anon': '20/s',  # 会去配置的 UserRateThrottle 以及 AnonRateThrottle 中找到属性 scope ，scope对应的就是生效的配置
        'user': '50/s'
    },
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=120),  # 访问令牌的有效时间
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),  # 刷新令牌的有效时间
    'ROTATE_REFRESH_TOKENS': False,  # 若为 True，则刷新后新的 refresh_token 有更新的有效时间
    'BLACKLIST_AFTER_ROTATION': True,  # 若为 True，刷新后的 token 将添加到黑名单中,
    'ALGORITHM': 'HS256',  # 对称算法：HS256 HS384 HS512  非对称算法：RSA
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,  # if signing_key, verifying_key will be ignored.
    'AUDIENCE': None,
    'ISSUER': None,
    'AUTH_HEADER_TYPES': ('Bearer',),  # Authorization: Bearer <token>
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',  # if HTTP_X_ACCESS_TOKEN, X_ACCESS_TOKEN: Bearer <token>
    'USER_ID_FIELD': 'id',  # 使用唯一不变的数据库字段，将包含在生成的令牌中以标识用户
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),  # default: access
    'TOKEN_TYPE_CLAIM': 'token_type',  # 用于存储令牌唯一标识符的声明名称 value:'access','sliding','refresh'
    'JTI_CLAIM': 'jti',
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',  # 滑动令牌是既包含到期声明又包含刷新到期声明的令牌
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),  # 只要滑动令牌的到期声明中的时间戳未通过，就可以用来证明身份验证
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),  # path('token|refresh', TokenObtainSlidingView.as_view())
}

# cors 配置
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = ('*',)
# 允许所有 域名/IP 跨域
CORS_ALLOW_ALL_ORIGINS = True
# 配置可跨域访问的 域名/IP
# CORS_ALLOWED_ORIGINS = [
#     '*',
# ]
# 配置允许的请求方式
CORS_ALLOW_METHODS = [
    '*',  # * 表示允许全部请求头
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS'
]
CORS_EXPOSE_HEADERS = [
    'Content-Disposition',
]

# log
LOG_DIR = BASE_DIR / 'logs'
if not LOG_DIR.exists():
    LOG_DIR.mkdir()

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # 禁用已经存在的 logger 实例
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    # 定义了两种日志格式
    'formatters': {
        # 详细
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{'
        },
        # 简单
        'simple': {
            'format': '%(asctime)s %(levelname)s %(name)s %(process)d %(thread)d %(message)s',
        },
    },
    'handlers': {
        # 发送邮件，只有 debug=False 且 Error 级别以上发邮件
        'mail': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
        # 保存到日志文件
        'file': {
            'level': 'INFO',
            'class': 'utils.log_handler.ConcurrentRotatingFileHandler',  # 滚动生成日志，切割
            'filename': LOG_DIR / 'domo.log',  # 日志文件名
            'maxBytes': 5 * 1024 * 1024,  # 单个日志文件最大为 5M
            'backupCount': 10,  # 日志备份文件最大数量
            'formatter': 'simple',  # 简单格式
            'encoding': 'utf-8',  # 防止中文乱码
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['file'],
    },
}

# 读取系统版本
version_file = BASE_DIR / 'version.txt'
if version_file.exists():
    with open(version_file, 'r') as f:
        SYSTEM_VERSION = f.read().strip()
else:
    SYSTEM_VERSION = 'unknown'
DEV = False

# 文章相关配置
ARTICLE_APP = {
    'IMG_EXTENSIONS': ('jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff'),  # 上传图片限制
    'MAX_IMAGE_SIZE': 1024 * 1024 * 10,
    'IMG_SAVE_DIR': Path('static/article_app/img'),
    'MD_FILE_SAVE_DIR': Path('static/article_app'),
    'MD_FILE_MAX_SIZE': 1024 * 1024 * 20,
}

# 文件相关配置
FILE_APP = {
    'MAX_FILE_SIZE': 1024 * 1024 * 50,
    'FILE_SAVE_DIR': Path('static/file_app'),
}

VIDEO_APP = {
    'VIDEO_DIR': Path('static/video_app'),
}

# 壁纸相关配置
WALLPAPER_APP = {
    'MAX_SIZE': 1024 * 1024 * 30,
    'SAVE_DIR': Path('static/wallpaper_app'),
    'THUMB_SAVE_DIR': Path('static/wallpaper_app/thumb'),
}
