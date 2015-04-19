from functools import wraps
import os

from fabric.api import abort, cd, env, local, run, task
from fabric.context_managers import path
from fabvenv import virtualenv

env.use_ssh_config = True

_defaults = {
    'branch': 'master',
    'repository': 'git@github.com:MarkusH/blog.git',

    'deploy_dir': None,
    'repo_dir': None,
    'sass_dir': None,
    'venv_dir': None,
}
for k, v in _defaults.items():
    env.setdefault(k, v)


def verify_remote(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if env.deploy_dir is None:
            abort('No deploy_dir specified')
        if env.repo_dir is None:
            abort('No repo_dir specified')
        if env.sass_dir is None:
            abort('No sass_dir specified')
        if env.venv_dir is None:
            abort('No venv_dir specified')
        func(*args, **kwargs)

    return wrapper


@task
@verify_remote
def git():
    """
    Installs and updates all requirements.
    """
    with cd(env.repo_dir):
        run('git pull')
        run('git submodule init')
        run('git submodule update')


@task
@verify_remote
def update():
    """
    Installs and updates all requirements.
    """
    with cd(env.repo_dir), virtualenv(env.venv_dir):
        run('pip install -r requirements.txt')
        run('npm install')
        run('./node_modules/bower/bin/bower install')


@task
@verify_remote
def build_remote():
    """
    Deploys the latest changes:

    1. Builds CSS/JS
    2. Builds HTML
    3. Rsync data
    """
    with cd(env.repo_dir), path(env.sass_dir), virtualenv(env.venv_dir):
        run('./node_modules/grunt-cli/bin/grunt')
        run('pelican -o dist -s publishconf.py content')
        # run('rsync -a ./dist/ {deploy_dir}'.format(**env))


@task
@verify_remote
def deploy():
    git()
    update()
    build_remote()


@task
def clean():
    """
    Cleans local build directory.
    """
    if os.path.isdir('build'):
        local('rm -rf build/*')
        local('mkdir -p build')


@task
def grunt():
    """
    Runs grunt locally
    """
    local('./node_modules/grunt-cli/bin/grunt')


@task
def pelican():
    """
    Runs pelican locally
    """
    local('pelican -o build -s pelicanconf.py content')


@task
def build():
    """
    Builds the page.
    """
    grunt()
    pelican()


@task
def serve():
    """
    Runs a local HTTP server.
    """
    local('cd {deploy_path} && python -m SimpleHTTPServer'.format(**env))
