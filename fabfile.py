from fabric.api import *
import fabric.contrib.project as project
import os

# Local path configuration (can be absolute or relative to fabfile)
env.content_path = 'content'
env.deploy_path = 'build'
DEPLOY_PATH = env.deploy_path

# Remote server configuration
production = 'markusholtermann.eu'
dest_path = '/srv/http/markusholtermann.eu'


def clean():
    if os.path.isdir(DEPLOY_PATH):
        local('rm -rf {deploy_path}/*'.format(**env))
        local('mkdir {deploy_path}'.format(**env))

def build():
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
    local('pelican -o {deploy_path} -s publishconf.py {content_path}'.format(**env))

@hosts(production)
def publish():
    local('pelican -o {deploy_path} -s publishconf.py {content_path}'.format(**env))
    project.rsync_project(
        remote_dir=dest_path,
        local_dir=DEPLOY_PATH.rstrip('/') + '/',
        delete=True
    )
