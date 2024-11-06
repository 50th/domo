# Domo

## 功能列表

- [x] 首页
  - [x] 文章浏览量前 5 展示
  - [x] 文件下载量前 5 展示
- [x] 文章
  - [x] 文章列表
  - [x] 添加文章
  - [x] 修改文章
  - [x] 删除文章
  - [x] 上传文章
  - [x] 文章编辑记录
  - [x] 文章浏览记录
  - [ ] 文章点赞
- [x] 文件
  - [x] 文件列表
    - [x] 查看权限
      - 公共文件都能查看
      - 登录用户文件可以额外查看自己的文件
      - 管理员可以查看所有文件
    - [x] 显示下载次数
    - [x] 排序，支持：
      - 文件名
      - 文件大小
      - 上传时间
  - [x] 文件上传，非登录用户只能上传小于 5M 的文件
  - [x] 文件下载
    - 公共文件都能下载
    - 登录用户文件可以额外下载自己的文件
    - 管理员可以下载所有文件
  - [x] 文件删除
    - 公共文件都能删除
    - 登录用户文件可以删除自己的文件
    - 管理员可以删除所有文件
  - [x] 文件下载记录
- [x] 壁纸
  - [x] 上传壁纸
    - 转为 JPG 格式保存
    - 保存缩略图
  - [x] 壁纸展示
    - 缩略图
    - 大图预览
  - [x] 删除壁纸
  - [x] 下载壁纸
- [ ] 视频
  - [x] 视频上传，使用 ffmpeg 获取视频时长
  - [x] 视频播放
  - [ ] 视频转码
- [ ] 工具
- [x] about
  - 每日一言
- [x] 404
- [x] docker 部署

## 运行

### 后端

1. 进入 domo 目录
2. 使用 python 3.9.2 及以上
3. 安装依赖库：`pip install -r requirements_dev.txt -i https://pypi.doubanio.com/simple`
4. 从 <https://github.com/BtbN/FFmpeg-Builds/releases> 下载 FFMPEG 可执行文件，放入 utils/ffmpeg 目录下
5. 初始化数据库：
   - `python manage.py makemigrations -settings=domo.settings.dev`
   - `python manage.py migrate -settings=domo.settings.dev`
6. 启动：`python manage.py runserver -settings=domo.settings.dev`

注意：**由于 django 的 StatReloader 会加载 settings 打开日志文件，导致在 windows 下日志滚动时无法移动日志文件，但部署是在 linux 中，不会有影响**

### 前端

1. 进入 domo_front 目录
2. 依赖 node 版本：20.12.2 及以上
3. 安装依赖：`npm run install`
4. 启动：`npm run dev`

## 打包

1. 修改`version.txt`文件中的版本号
2. 执行`pack.sh`脚本打包
3. 默认`domo_x.x.x.zip`打包到 deploy 目录下

## 部署

1. 准备好 docker 环境
2. 创建 domo 目录
3. 将`domo_x.x.x.zip`上传到 domo 目录下并解压：`unzip -o domo_x.x.x.zip`
4. 执行`bash install.sh`脚本部署服务
