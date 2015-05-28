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
def bootstrap():
    """
    Remote -- Bootstrap git repo, virtualenv, sass, grunt, bower
    """
    run('mkdir -p {repo_dir}'.format(**env))
    with cd(env.repo_dir):
        run('git clone {repository} .'.format(**env))
        run('git checkout {branch}'.format(**env))
        run('virtualenv {venv_dir}'.format(**env))
        run('gem install --user-install sass:3.4.13')
    update()


@task
@verify_remote
def git():
    """
    Remote -- Installs and updates all requirements.
    """
    with cd(env.repo_dir):
        run('git pull')
        run('git checkout -f {branch}'.format(**env))
        run('git submodule init')
        run('git submodule update')


@task
@verify_remote
def update():
    """
    Remote -- Installs and updates all requirements.
    """
    with cd(env.repo_dir), virtualenv(env.venv_dir):
        run('pip install -r requirements.txt')
        run('npm install')


@task
@verify_remote
def build_remote():
    """
    Remote -- Deploys the latest changes.
    """
    with cd(env.repo_dir), path(env.sass_dir), virtualenv(env.venv_dir):
        run('./node_modules/grunt-cli/bin/grunt')
        run('pelican -o dist -s publishconf.py content')


@task
@verify_remote
def rsync():
    """
    Remote -- Rsync
    """
    with cd(env.repo_dir):
        run('rsync -av ./dist/ {deploy_dir}'.format(**env))


@task
@verify_remote
def deploy():
    """
    Remote -- Do everything needed to deploy: git, update, build_remote, rsync
    """
    git()
    update()
    build_remote()
    rsync()


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
    local('pelican -o build -s pelicanconf.py content --ignore-cache')


@task
def build():
    """
    Builds the page locally
    """
    grunt()
    pelican()


@task
def serve():
    """
    Runs a local HTTP server.
    """
    local('cd build && python -m SimpleHTTPServer')
