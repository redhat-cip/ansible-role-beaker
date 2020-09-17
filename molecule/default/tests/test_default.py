import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


#@pytest.mark.parametrize('protocol,port', [
#    ('tcp', '53'),
#    ('udp', '53'),
#    ('udp', '67'),
#    ('udp', '69'),
#    ('tcp', '80'),
#    ('tcp', '3306'),
#    ('tcp', '8000'),
#    ('unix', '/var/lib/mysql/mysql.sock')
#])
#def test_listening_socket(host, protocol, port):
#    socket = host.socket('%s://%s' % (protocol, port))
#    assert socket.is_listening


@pytest.mark.parametrize('service_name', [
    'beakerd', 'beaker-provision', 'beaker-proxy',
    'beaker-watchdog', 'httpd', 'mariadb'
])
def test_services_running_and_enabled(host, service_name):
    service = host.service(service_name)
    assert service.is_running
    assert service.is_enabled


@pytest.mark.parametrize('package_name', [
    'beaker-client', 'beaker-lab-controller', 'beaker-server',
    'httpd', 'mariadb-server'
])
def test_package_installed(host, package_name):
    package = host.package(package_name)
    assert package.is_installed


def test_mariadb_default_charset(host):
    f = host.file('/etc/my.cnf')
    assert f.exists
    assert f.is_file
    assert f.user == 'root'
    assert f.group == 'root'
    assert f.mode == 0o644
    assert f.contains('character-set-server = utf8')


#def test_beaker_init(host):
#    with host.sudo():
#        assert host.run('beaker-init --check').rc == 0


#def test_labcontrol_is_populated(host):
#    with host.sudo():
#        ret = host.run('bkr labcontroller-list')
#        assert ret.rc == 0
#        assert ret.stdout


#def test_beaker_tasks_list(host):
#    tasks_expected = {
#        '/distribution/check-install',
#        '/distribution/command',
#        '/distribution/inventory',
#        '/distribution/pkginstall',
#        '/distribution/rebuild',
#        '/distribution/reservesys',
#        '/distribution/updateDistro',
#        '/distribution/utils/dummy',
#        '/distribution/virt/image-install',
#        '/distribution/virt/install',
#        '/distribution/virt/start',
#        '/distribution/virt/start_stop',
#        '/distribution/virt/stop',
#        '/kernel/distribution/ltp-nfs/ltp',
#    }
#    with host.sudo():
#        bkr_task_list_ret = host.run('bkr task-list')
#        tasks_found = set(bkr_task_list_ret.stdout.rstrip('\n').split('\n'))
#        assert tasks_found == tasks_expected


#def test_httpd_bkr(host):
#    assert host.ansible(
#        "uri",
#        "url=http://localhost/bkr/",
#        check=False)['status'] == 200
#    assert host.ansible(
#        "uri",
#        "url=http://localhost/beaker/",
#        check=False)['status'] == 200
