import os

from fabric.api import local
from fabric.decorators import task
from fabric.context_managers import cd, prefix
from fabric.operations import sudo, run, put

circus_file_path = os.path.realpath('deploy/circus.ini')
circus_service_file_path = os.path.realpath('deploy/circus.service')
nginx_config_path = os.path.realpath('deploy/nginx')
nginx_avaliable_path = "/etc/nginx/sites-available/"
nginx_enable_path = "/etc/nginx/sites-enabled/"
app_path = "~"
prod_settings_path = os.path.realpath('growth_studio/prod_settings.py')


@task
def install(requirements_env="dev"):
    """ Install requirements packages """
    local('pip install -r requirements/%s.txt' % requirements_env)


@task
def runserver():
    """ Run Server """
    local('./manage.py runserver')


@task
def lint():
    """ Check the project for Flake8 compliance using `flake8` """
    local('flake8 --config .flake8')


@task
def test():
    """ Run Test """
    local('./manage.py test')


@task
def tag_version(version):
    """ Tag New Version """
    local('git tag v%s' % version)
    local('git push origin v%s' % version)


@task
def fetch_version(version):
    """ Fetch Git Version """
    local('wget '
          'https://codeload.github.com/travelgeezer/sasukekun/tar.gz/'
          '%s' % version)


@task
def host_type():
    run('uname -a')


@task
def setup():
    """ Setup the Ubuntu Env """
    sudo('apt-get install python-software-properties')
    sudo('add-apt-repository ppa:jonathonf/python-3.6')
    sudo('apt-get update')
    APT_GET_PACKAGES = [
        'build-essential',
        'git',
        'python3.6',
        'python3.6-dev',
        'python3.6-venv',
        'nginx',
        # 'mysql-server',
        'libmysqlclient-dev',
    ]
    sudo('apt-get install -y ' + ' '.join(APT_GET_PACKAGES))
    sudo('wget https://bootstrap.pypa.io/get-pip.py')
    sudo('python3.6 get-pip.py')
    # sudo('ln -s /usr/bin/python3.6 /usr/local/bin/python3')
    # sudo('ln -s /usr/local/bin/pip /usr/local/bin/pip3')
    sudo('update-alternatives --install /usr/bin/python python /usr/bin/python2 100')
    sudo('update-alternatives --install /usr/bin/python python /usr/bin/python3.6 150')
    sudo('pip install pipenv -i https://mirrors.aliyun.com/pypi/simple')
    sudo('pip install circus -i https://mirrors.aliyun.com/pypi/simple')
    sudo('pip install gunicorn -i https://mirrors.aliyun.com/pypi/simple')

    sudo('rm ' + nginx_enable_path + 'default')


def nginx_restart():
    """ Reset nginx """
    sudo("service nginx restart")


def nginx_start():
    """ Start nginx """
    sudo('service nginx start')


def nginx_config(nginx_config_path=nginx_config_path):
    """ Send nginx configuration """
    for file_name in os.listdir(nginx_config_path):
        put(os.path.join(nginx_config_path, file_name),
            nginx_avaliable_path, use_sudo=True)


def circus_config():
    """ Send Circus configuration """
    sudo('mkdir -p /etc/circus/')
    put(circus_file_path, '/etc/circus/', use_sudo=True)


def circus_service_config():
    """ Send Circus Service configuration """
    put(circus_service_file_path, '/etc/systemd/system/', use_sudo=True)


def circus_service_start():
    """ start circus service """
    sudo('systemctl start circus')
    sudo('systemctl --system daemon-reload')
    sudo('systemctl restart circus')


def nginx_enable_site(nginx_config_file):
    "Enable nginx site"
    with cd(nginx_enable_path):
        sudo('rm -f ' + nginx_config_file)
        sudo('ln -s ' + nginx_avaliable_path + nginx_config_file)


@task
def deploy(version):
    """ depoly app to cloud """
    with cd(app_path):
        get_app(version)
        setup_app(version)
        config_app()

    nginx_config()
    nginx_enable_site('sasukekun.conf')

    circus_config()
    circus_service_config()

    circus_service_start()

    nginx_restart()


def copy_prod_settings():
    with cd(app_path):
        put(prod_settings_path, '/home/ubuntu/sasukekun/growth_studio/')


def config_app():
    copy_prod_settings()
    with cd('sasukekun'):
        run('pipenv install')
        run('pipenv install gunicorn==19.4.5')
        run('pipenv run python manage.py collectstatic -l --noinput')
        run('pipenv run python manage.py makemigrations')
        run('pipenv run python manage.py migrate')


def setup_app(version):
    run('rm -rf sasukekun')
    run('ln -s sasukekun-%s sasukekun' % version)


def get_app(version):
    run(('wget '
         'https://codeload.github.com/travelgeezer/sasukekun/tar.gz/v'
         '%s') % version)
    run('tar xvf v%s' % version)
