import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_beaker_services_running_and_enabled(host):
    services = ['beaker-provision', 'beaker-proxy',
                'beaker-watchdog', 'beakerd']
    for service_name in services:
        service = host.service(service_name)
        assert service.is_running
        assert service.is_enabled


def test_beakerd_tcp_socket(host):
    socket = host.socket('tcp://:::8000')
    assert socket.is_listening


def test_dnsmasq_running_and_enabled(host):
    service = host.service('dnsmasq')
    assert service.is_running
    assert service.is_enabled


def test_dns_all_socket(host):
    tcp = host.socket('tcp://:::53')
    udp = host.socket('udp://:::53')
    assert tcp.is_listening
    assert udp.is_listening


def test_dhcp_udp_socket(host):
    socket = host.socket('udp://:::67')
    assert socket.is_listening


def test_tftp_udp_socket(host):
    socket = host.socket('udp://:::69')
    assert socket.is_listening


def test_httpd_running_and_enabled(host):
    service = host.service('httpd')
    assert service.is_running
    assert service.is_enabled


def test_httpd_tcp_socket(host):
    socket = host.socket('tcp://:::80')
    assert socket.is_listening


def test_mariadb_default_charset(host):
    f = host.file('/etc/my.cnf')
    assert f.exists
    assert f.is_file
    assert f.user == 'root'
    assert f.group == 'root'
    assert f.mode == 0o644
    assert f.contains('character-set-server = utf8')


def test_mariadb_running_and_enabled(host):
    service = host.service('mariadb')
    assert service.is_running
    assert service.is_enabled


def test_mariadb_package(host):
    package = host.package('mariadb-server')
    assert package.is_installed


def test_mariadb_unix_socket(host):
    socket = host.socket('unix:///var/lib/mysql/mysql.sock')
    assert socket.is_listening


def test_mariadb_tcp_socket(host):
    socket = host.socket('tcp://0.0.0.0:3306')
    assert socket.is_listening


def test_beaker_init(host):
    with host.sudo():
        assert host.run('beaker-init --check').rc == 0


def test_labcontrol_is_populated(host):
    with host.sudo():
        ret = host.run('bkr labcontroller-list')
        assert ret.rc == 0
        assert ret.stdout


def test_beaker_tasks_list(host):
    tasks_expected = {
        '/distribution/check-install',
        '/distribution/command',
        '/distribution/install',
        '/distribution/inventory',
        '/distribution/pkginstall',
        '/distribution/rebuild',
        '/distribution/reservesys',
        '/distribution/updateDistro',
        '/distribution/utils/dummy',
        '/distribution/virt/image-install',
        '/distribution/virt/install',
        '/distribution/virt/start',
        '/distribution/virt/start_stop',
        '/distribution/virt/stop',
        '/kernel/distribution/ltp-nfs/ltp',
    }
    with host.sudo():
        bkr_task_list_ret = host.run('bkr task-list')
        tasks_found = set(bkr_task_list_ret.stdout.split('\n'))
        assert tasks_found == tasks_expected


def test_httpd_bkr(host):
    assert host.ansible(
        "uri",
        "url=http://localhost/bkr/",
        check=False)['status'] == 200
    assert host.ansible(
        "uri",
        "url=http://localhost/beaker/",
        check=False)['status'] == 200
