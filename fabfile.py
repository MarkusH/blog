from fabric.api import *
import fabric.contrib.project as project
import os

# Local path configuration (can be absolute or relative to fabfile)
env.content_path = 'content'
env.deploy_path = 'build'


def clean():
    if os.path.isdir(env.deploy_path):
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
    env.deploy_path = 'dist'
    project.rsync_project(
        remote_dir=env.dest_path,
        local_dir=env.deploy_path.rstrip('/') + '/',
        delete=True,
        ssh_opts='-i /home/markus/.ssh/id_rsa-vserver',
    )


def publish():
    env.deploy_path = 'dist'
    preview()
    rsync()
