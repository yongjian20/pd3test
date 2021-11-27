#!/usr/bin/env sh

set -x
#cp -r /var/jenkins_home/workspace/dabestteam_pipeline ${WORKSPACE}/jenkins

# docker build -t basic-flask:latest --build-arg APP_IMAGE=python:3.9 -f Dockerfile .
docker build -t basic-flask:latest --build-arg APP_IMAGE=ubuntu -f Dockerfile .

sleep 1
set +x

echo 'Now...'
echo 'Visit http://139.59.252.115:8081 to see your web application in action.'
