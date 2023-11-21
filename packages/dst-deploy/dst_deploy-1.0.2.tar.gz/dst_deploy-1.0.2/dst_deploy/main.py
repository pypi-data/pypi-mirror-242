"""main"""
import logging

from .steam import init_dst_server
from .dst import DstServer
from .settings import STEAM_PATH, DST_SERVER_PATH, DST_APPID


log = logging.getLogger(__name__)


def deploy(cluster: str):
    """部署启动饥荒服务.

    Args:
        cluster (str): 存档名称.
    """
    log.info("#### dst deploy start ####")
    init_dst_server(STEAM_PATH, DST_SERVER_PATH, DST_APPID)
    dst = DstServer(DST_SERVER_PATH, cluster=cluster)
    dst.run()
    while True:
        try:
            log.info(f"[master]: {dst.master.stdout.readline()}")
        except Exception as e:
            log.exception(f"dst server run err: {e}")


if __name__ == "__main__":
    deploy("Cluster_1")