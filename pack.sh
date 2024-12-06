#!/usr/bin/bash

version=`cat version.txt`
echo "出包版本 $version"
echo "前端页面打包"
cd domo_front
npm install
npm run build
rm -f dist.zip
zip -qr dist.zip dist
mv dist.zip ../
cd ..
# 删除 __pycache__ 文件夹
# find . -path ./venv -prune -o -name '__pycache__' -type d -exec rm -r {} +
# zip -qr domo_backend.zip app_article app_file app_user constants domo utils gunicorn.py manage.py requirements_pro.txt
echo "构建后端 docker 镜像"
cp -f version.txt domo/version.txt
docker build -t domo_app:"$version" .
echo "保存 docker 镜像"
docker save -o domo_app_"$version".tar domo_app:"$version"
sed -i "s/image: domo_app:.*/image: domo_app:${version}/" docker-compose.yml
rm -f domo*.zip
echo "打包镜像和前端页面"
zip -qr domo.zip docker-compose.yml domo_app_"$version".tar dist.zip nginx version.txt
zip -qr domo_"$version".zip domo.zip install.sh
if [ ! -d "deploy" ]; then
    mkdir deploy
fi
mv -f domo_"$version".zip deploy/
rm -f domo_app*.tar dist.zip domo.zip
echo "出包完成 $version"
