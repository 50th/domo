#!/usr/bin/bash

port=80
container_id=$(docker ps -q -f "publish=$port" -f "name=domo_nginx")
if [ "$container_id" == "" ];then
    if lsof -i :$port | grep LISTEN >/dev/null
    then
        echo "$port 端口被占用"
        exit 1
    fi
fi
echo "解压程序文件"
unzip -oq domo.zip
version=`cat version.txt`
echo "安装版本：$version"
echo "部署前端页面文件"
unzip -oq dist.zip
rm -rf domo_front
mv -f dist domo_front
echo "获取旧版本镜像"
oldImageID=`docker images | grep "domo_app" | awk '{print $3}'`
echo "加载 docker 镜像"
docker load -i domo_app_"$version".tar
echo "启动 docker 容器"
docker-compose up -d
docker-compose restart
echo "删除旧版本镜像"
if [[ "$oldImageID" != "" ]]; then
    # 检查镜像是否被使用
    if [[ -z $(docker ps -a -q --filter "ancestor=$oldImageID") ]]; then
        docker rmi $oldImageID
    fi
fi
echo "清理环境"
rm -f domo_app_"$version".tar dist.zip domo.zip
rm -f install.sh
echo "安装完成"
