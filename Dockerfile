FROM python:3.9.18-slim-bullseye

# 工作目录
WORKDIR /usr/local/domo

# 复制代码
COPY ./domo /usr/local/domo
# 安装依赖库
RUN pip install --no-cache-dir -r requirements_pro.txt -i https://mirrors.aliyun.com/pypi/simple/ && pip cache purge
RUN mkdir logs
# 暴露端口
EXPOSE 8899
# 环境变量
ENV DJANGO_SETTINGS_MODULE domo.settings.pro
ENV PYTHONUNBUFFERED 1
# 启动命令
CMD ["bash", "start.sh"]
