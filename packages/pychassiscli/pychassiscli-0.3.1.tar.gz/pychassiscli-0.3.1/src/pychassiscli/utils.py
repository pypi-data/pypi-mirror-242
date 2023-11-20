import os
import shutil
from time import sleep
from contextlib import contextmanager

from mako.template import Template
from rich import print as rich_print
from python_on_whales import DockerException, ClientNotFoundError, DockerClient


docker = DockerClient()


def check_docker():
    """
    Check if docker and docker compose are installed and running.
    """
    try:
        docker.ps()
    except ClientNotFoundError:
        rich_print('Please install docker firstly')
        raise
    except DockerException:
        rich_print('Please start docker correctly')
        raise

    rich_print('[bold magenta]Docker is installed successfully[/bold magenta]', ":vampire:")

    if not docker.compose.is_installed():
        rich_print('Please install docker compose firstly')
        raise

    rich_print('[bold magenta]Docker Compose is installed successfully[/bold magenta]', ":vampire:")


@contextmanager
def status(status_msg: str, newline: bool = False, quiet: bool = False):
    """
    Show status message and yield.
    """
    msg_suffix = ' ...' if not newline else ' ...\n'
    rich_print(status_msg + msg_suffix)
    try:
        yield
    except Exception as e:
        if not quiet:
            rich_print('  [bold magenta]FAILED[/bold magenta]\n')
        raise
    else:
        if not quiet:
            rich_print('  [bold magenta]Done[/bold magenta]\n')


def get_directory(dir_name: str) -> str:
    """
    Return the directory path of the given pychassiscli directory name.
    """
    import pychassiscli

    package_dir = os.path.abspath(os.path.dirname(pychassiscli.__file__))
    return os.path.join(package_dir, dir_name)


def copy_files(src_dir, dest_dir):
    for file_ in os.listdir(src_dir):
        if file_ == '__pycache__':
            continue

        src_file_path = os.path.join(src_dir, file_)
        output_file = os.path.join(dest_dir, file_)
        if os.path.isdir(src_file_path):
            if not os.access(output_file, os.F_OK):
                with status(f'Creating directory {os.path.abspath(output_file)!r}'):
                    os.makedirs(output_file)
            copy_files(src_file_path, output_file)
        else:
            with status(f'Generating {os.path.abspath(output_file)}'):
                shutil.copy(src_file_path, output_file)


def template_to_file(
        template_file: str, dest: str, output_encoding: str, **kw
) -> None:
    template = Template(filename=template_file)
    try:
        output = template.render_unicode(**kw).encode(output_encoding)
    except Exception as e:
        rich_print('Template rendering failed.')
        raise
    else:
        with open(dest, "wb") as f:
            f.write(output)


def start_network(network_name):
    with status(f'Starting network {network_name}'):
        docker.network.create(network_name, driver='bridge')


def stop_network(network_name):
    with status(f'Stopping network {network_name}'):
        docker.network.remove(network_name)


def start_metric_network():
    start_network('metric_servers')


def stop_metric_network():
    stop_network('metric_servers')


def start_statsd_agent():
    with status(f'Starting statsd agent'):
        metric_configs_dir = os.path.join(get_directory('chassis-agent'), 'metric-configs')
        statsd_config_file_path = os.path.join(metric_configs_dir, 'statsd_config.js')
        returned_string = docker.run(image='statsd/statsd:latest', name='statsd-agent', hostname='statsd-agent',
                                     detach=True, restart='always', interactive=True, tty=True,
                                     publish=[(8125, 8125, 'udp'), (8126, 8126)], pull='missing',
                                     volumes=[(statsd_config_file_path, '/usr/src/app/config.js', 'rw')],
                                     networks=['metric_servers'])
        rich_print('\nContainer ID: ' + '[bold magenta]' + str(returned_string) + '[/bold magenta]' + '\n')


def start_statsd_exporter():
    with status(f'Starting statsd exporter'):
        statsd_mapping_file_path = os.getcwd() + '/statsd_mapping.yml'
        returned_string = docker.run(image='prom/statsd-exporter:latest', name='statsd-exporter', pull='missing',
                                     detach=True, restart='always', tty=True, hostname='statsd-exporter',
                                     publish=[(9125, 9125, 'udp'), (9102, 9102)], interactive=True,
                                     command=['--statsd.mapping-config=/tmp/statsd_mapping.yml'],
                                     volumes=[(statsd_mapping_file_path, '/tmp/statsd_mapping.yml', 'rw')],
                                     networks=['metric_servers'])
        rich_print('\nContainer ID: ' + '[bold magenta]' + str(returned_string) + '[/bold magenta]' + '\n')


def start_prometheus():
    with status(f'Starting prometheus'):
        prometheus_conf_dir = os.path.join(get_directory('chassis-agent'), 'metric-configs')
        prometheus_conf_file_path = os.path.join(prometheus_conf_dir, 'prometheus_conf/prometheus.yml')
        returned_string = docker.run(image='prom/prometheus:latest', name='prometheus', hostname='prometheus',
                                     detach=True, restart='always', tty=True, interactive=True,
                                     publish=[(9193, 9090)], pull='missing',
                                     volumes=[(prometheus_conf_file_path, '/etc/prometheus/prometheus.yml', 'rw')],
                                     networks=['metric_servers'])
        rich_print('\nContainer ID: ' + '[bold magenta]' + str(returned_string) + '[/bold magenta]' + '\n')


def start_grafana():
    with status(f'Starting grafana'):
        grafana_conf_dir = os.path.join(get_directory('chassis-agent'), 'metric-configs')
        grafana_provisioning_path = os.path.join(grafana_conf_dir, 'grafana_conf/provisioning')
        grafana_config_path = os.path.join(grafana_conf_dir, 'grafana_conf/config/grafana.ini')
        grafana_dashboard_path = os.path.join(os.getcwd(), 'grafana_dashboards')
        returned_string = docker.run(image='grafana/grafana:latest', name='grafana', hostname='grafana',
                                     detach=True, restart='always', tty=True, interactive=True,
                                     publish=[(3100, 3000)], pull='missing',
                                     volumes=[(grafana_provisioning_path, '/etc/grafana/provisioning', 'rw'),
                                              (grafana_config_path, '/etc/grafana/grafana.ini', 'rw'),
                                              (grafana_dashboard_path, '/var/lib/grafana/dashboards', 'rw')],
                                     networks=['metric_servers'])
        rich_print('\nContainer ID: ' + '[bold magenta]' + str(returned_string) + '[/bold magenta]' + '\n')


def start_metric_servers():
    # TODO 检查相应容器是否已启动，如果启动，则先删除
    start_network('metric_servers')
    sleep(0.25)
    start_prometheus()
    sleep(0.25)
    start_statsd_exporter()
    sleep(0.25)
    start_statsd_agent()
    sleep(0.25)
    start_grafana()


def stop_statsd_agent():
    with status(f'Stopping statsd agent'):
        docker.remove('statsd-agent', force=True)
        rich_print('\nContainer is [bold magenta]removed[/bold magenta].' + '\n')


def stop_statsd_exporter():
    with status(f'Stopping statsd exporter'):
        docker.remove('statsd-exporter', force=True)
        rich_print('\nContainer is removed.' + '\n')


def stop_prometheus():
    with status(f'Stopping prometheus'):
        docker.remove('prometheus', force=True)
        rich_print('\nContainer is removed.' + '\n')


def stop_grafana():
    with status(f'Stopping grafana'):
        docker.remove('grafana', force=True)
        rich_print('\nContainer is removed.' + '\n')


def stop_metric_servers():
    stop_statsd_agent()
    sleep(0.25)
    stop_statsd_exporter()
    sleep(0.25)
    stop_prometheus()
    sleep(0.25)
    stop_grafana()
    sleep(0.25)
    stop_network('metric_servers')


def refresh_metric_servers():
    stop_statsd_exporter()
    sleep(0.25)
    stop_grafana()
    sleep(0.25)
    start_statsd_exporter()
    sleep(0.25)
    start_grafana()


if __name__ == '__main__':
    with status(f'Generating Test'):
        pass