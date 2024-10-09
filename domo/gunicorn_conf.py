import multiprocessing
import os

if not os.path.exists('logs'):
    os.mkdir('logs')

bind = '0.0.0.0:8899'
workers = multiprocessing.cpu_count() * 2 + 1 if multiprocessing.cpu_count() <= 4 else 9
backlog = 2048
debug = False
timeout = 500
daemon = False  # 在创建容器时，需要保持前台，否则容器会直接结束运行
pidfile = './logs/gunicorn.pid'
logconfig_dict = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {'level': 'INFO', 'handlers': ['console']},
    'loggers': {
        'gunicorn.error': {
            'level': 'INFO',
            'handlers': ['error_file'],
            'propagate': False,
            'qualname': 'gunicorn.error'
        },
        'gunicorn.access': {
            'level': 'INFO',
            'handlers': ['access_file'],
            'propagate': False,
            'qualname': 'gunicorn.access'
        }
    },
    'handlers': {
        # 必须配置 console，root logger 默认使用 console handler
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'generic',
            'stream': 'ext://sys.stdout'
        },
        'error_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': './logs/gunicorn.error.log',
            'maxBytes': 5 * 1024 * 1024,
            'backupCount': 5,
            'formatter': 'generic'
        },
        'access_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': './logs/gunicorn.access.log',
            'maxBytes': 5 * 1024 * 1024,
            'backupCount': 5,
            'formatter': 'generic'
        },
    },
    'formatters': {
        'generic': {
            'format': '%(asctime)s [%(process)d] [%(levelname)s] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S %z',
            'class': 'logging.Formatter'
        }
    }
}
