from functools import wraps

from fabric.api import abort, cd, env, run, task
from fabric.context_managers import path
from fabvenv import virtualenv

env.use_ssh_config = True

_defaults = {
    'branch': 'master',
    'pelicanconf': 'publishconf.py',
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
    git()
    update()


@task
@verify_remote
def git():
    """
    Remote -- Installs and updates all requirements.
    """
    with cd(env.repo_dir):
        run('git checkout -f {branch}'.format(**env))
        run('git pull origin {branch}'.format(**env))
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
def grunt_remote():
    """
    Remote -- Runs Grunt
    """
    with cd(env.repo_dir), path(env.sass_dir):
        run('make grunt')


@task
@verify_remote
def pelican_remote():
    """
    Remote -- Runs Pelican
    """
    with cd(env.repo_dir), virtualenv(env.venv_dir):
        run('make pelican -e PELICAN_SETTINGS={pelicanconf}'.format(**env))


@task
@verify_remote
def build_remote():
    """
    Remote -- Deploys the latest changes: grunt_remote, pelican_remote, zip_*_remote
    """
    grunt_remote()
    pelican_remote()


@task
@verify_remote
def rsync():
    """
    Remote -- Rsync
    """
    with cd(env.repo_dir):
        run('rsync -av --checksum ./build/ {deploy_dir}'.format(**env))


@task
@verify_remote
def zip_remote():
    """
    Remote -- Zips files
    """
    with cd(env.deploy_dir):
        run('''find . -type f -a -! -name "*.gz" -exec sh -c 'test "${0}" -nt "${0}.gz" && gzip --keep --force --verbose -9 ${0}' {} \;''')
        # Include "[SKIP] <file>  is up to date" debugging
        # run('''find . -type f -a -! -name "*.gz" -exec sh -c 'test "${0}" -nt "${0}.gz" && gzip --keep --force --verbose -9 ${0} || echo "[SKIP] ${0} is up to date"' {} \;''')


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
    zip_remote()
