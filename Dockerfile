FROM astral/uv:0.8-python3.13-bookworm-slim

# 工作目录
WORKDIR /usr/local/domo

# 复制代码
COPY ./domo /usr/local/domo
# 安装依赖库
# RUN pip install --no-cache-dir -r requirements_pro.txt -i https://mirrors.aliyun.com/pypi/simple/ && pip cache purge
RUN uv sync --no-dev --frozen --extra prod
RUN mkdir logs
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list  # 更改 apt 为国内源
# 暴露端口
EXPOSE 8899
# 环境变量
ENV DJANGO_SETTINGS_MODULE domo.settings.pro
ENV PYTHONUNBUFFERED 1
# 启动命令
CMD ["bash", "start.sh"]
