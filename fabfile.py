from fabric.api import *
import fabric.contrib.project as project
import os

# Local path configuration (can be absolute or relative to fabfile)
env.content_path = 'content'
env.deploy_path = 'build'
DEPLOY_PATH = env.deploy_path

dest_path = '/srv/http/markusholtermann.eu'


def clean():
    if os.path.isdir(DEPLOY_PATH):
        local('rm -rf {deploy_path}/*'.format(**env))
        local('mkdir -p {deploy_path}'.format(**env))


def grunt():
    local('./node_modules/grunt-cli/bin/grunt')


def build():
    grunt()
    local('pelican -o {deploy_path} -s pelicanconf.py {content_path}'.format(**env))


def rebuild():
    clean()
    build()


def regenerate():
    local('pelican -o {deploy_path}  -r -s pelicanconf.py {content_path}'.format(**env))


def serve():
    local('cd {deploy_path} && python -m SimpleHTTPServer'.format(**env))


def reserve():
    build()
    serve()


def preview():
    grunt()
    local('pelican -o {deploy_path} -s publishconf.py {content_path}'.format(**env))


def rsync():
    project.rsync_project(
        remote_dir=dest_path,
        local_dir=DEPLOY_PATH.rstrip('/') + '/',
        delete=True,
        ssh_opts='-i /home/markus/.ssh/id_rsa-vserver',
    )


def publish():
    clean()
    preview()
    rsync()
