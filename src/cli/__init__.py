"""

"""

import click

from pathlib import Path
from typing import Any, Dict  # noqa: F401

from dcos_e2e.backends import Docker
from dcos_e2e.cluster import Cluster
from dcos_e2e.distributions import Distribution
from dcos_e2e.docker_versions import DockerVersion

_LINUX_DISTRIBUTIONS = {
    'centos-7': Distribution.CENTOS_7,
    'ubuntu-16.04': Distribution.UBUNTU_16_04,
    'coreos': Distribution.COREOS,
    'fedora-23': Distribution.FEDORA_23,
    'debian-8': Distribution.DEBIAN_8,
}


@click.group()
def dcos_docker() -> None:
    """
    Manage DC/OS clusters on Docker.
    """


@dcos_docker.command('create')
@click.argument('artifact', type=click.Path(exists=True))
@click.option('--suppress-output', is_flag=True, help='')
@click.option('--linux-distribution', type=click.Choice(_LINUX_DISTRIBUTIONS.keys()))
def create(artifact: str, suppress_output: bool) -> None:
    """
    Create a DC/OS cluster.
    """
    # Everything in this block should be a CLI option.
    custom_master_mounts = {}  # type: Dict[str, Dict[str, str]]
    custom_agent_mounts = {}  # type: Dict[str, Dict[str, str]]
    custom_public_agent_mounts = {}  # type: Dict[str, Dict[str, str]]
    linux_distribution = Distribution.COREOS
    docker_version = DockerVersion.v1_13_1
    docker_storage_driver = None
    # TODO this should also control Docker logs
    log_output_live = not suppress_output
    extra_config = {}  # type: Dict[str, Any]

    cluster_backend = Docker(
        custom_master_mounts=custom_master_mounts,
        custom_agent_mounts=custom_agent_mounts,
        custom_public_agent_mounts=custom_public_agent_mounts,
        linux_distribution=linux_distribution,
        docker_version=docker_version,
        storage_driver=docker_storage_driver,
    )

    cluster = Cluster(
        cluster_backend=cluster_backend,
        masters=1,
        agents=1,
        public_agents=1,
    )

    cluster.install_dcos_from_path(
        build_artifact=Path(artifact),
        extra_config=extra_config,
        log_output_live=log_output_live,
    )


if __name__ == '__main__':
    dcos_docker()
