__author__ = 'aub3'
from fabric.api import local,task,lcd
from fabric.state import env
import logging,time,datetime,os

ec2_AMI = ''
env.user = "ubuntu"
try:
    ec2_HOST = file("host").read().strip()
except:
    logging.warning("No EC2 host present")
    ec2_HOST = ""
    pass
env.key_filename = ""
env.hosts = [ec2_HOST,]


@task
def build():
    local('nvidia-docker build -t visualsearchservergpu .')


@task
def rm():
    try:
        local('nvidia-docker stop $(docker ps -a -q)')
    except:
        pass
    try:
        local('nvidia-docker rm $(docker ps -a -q)')
    except:
        pass
    local('nvidia-docker images -q --filter "dangling=true" | xargs docker rmi')
    local('nvidia-docker volume rm $(docker volume ls -qf dangling=true)')

@task
def start():
    local('nvidia-docker run -p 127.0.0.1:9000:9000 -p 127.0.0.1:8888:8888 -d -t visualsearchservergpu')


@task
def shell():
    local('nvidia-docker exec -u="root" -it $(docker ps -l -q) bash')


@task
def test():
    local('nvidia-docker exec -u="root" -it $(docker ps -l -q)  fab test')


@task
def server():
    test()
    local('nvidia-docker exec -u="root" -it $(docker ps -l -q)  fab server')


