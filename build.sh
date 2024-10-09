#!/usr/bin/bash

docker-compose down
unzip -o dist.zip
rm -rf domo_front
mv -f dist domo_front
docker-compose up -d
rm dist.zip domo_app.tar domo.zip