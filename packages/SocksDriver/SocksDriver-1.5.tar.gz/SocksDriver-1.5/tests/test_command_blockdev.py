from socket import gethostname
from psutil import disk_partitions, disk_usage
from SocksDriver import SocksClient


def test_command_blockdev_hostname(client: SocksClient) -> None:
    hostname = gethostname()
    for device in client.blockdev():
        assert hostname == device["host"]


def test_command_blockdev_num_partitions(client: SocksClient) -> None:
    results = client.blockdev()
    assert len(results) == len(disk_partitions())


def test_command_blockdev_mountpoint(client: SocksClient) -> None:
    # Use hash map to keep O(n) complexity
    partitions = {partition.device: partition for partition in disk_partitions()}

    for device in client.blockdev():
        assert device["mountpoint"] == partitions[device["mounted_device"]].mountpoint


def test_command_blockdev_fstype(client: SocksClient) -> None:
    partitions = {partition.device: partition for partition in disk_partitions()}

    for device in client.blockdev():
        assert device["fstype"] == partitions[device["mounted_device"]].fstype


def test_command_blockdev_total_size_from_statvfs(client: SocksClient) -> None:
    # Identical to $ df -B4096 --output=source,size

    for device in client.blockdev():
        assert device["total_size"] == disk_usage(device["mountpoint"]).total


def test_command_blockdev_available_size_from_statvfs(client: SocksClient) -> None:
    # Identical to $ df -B4096 --output=source,avail

    for device in client.blockdev():
        assert device["avail_size"] == disk_usage(device["mountpoint"]).free
