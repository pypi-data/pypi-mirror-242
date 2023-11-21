"""main"""
import logging

from .steam import init_dst_server
from .dst import DstServer
from .settings import STEAM_PATH, DST_SERVER_PATH, DST_APPID


log = logging.getLogger(__name__)


def main():
    """主函数"""
    log.info("#### dst deploy start ####")
    init_dst_server(STEAM_PATH, DST_SERVER_PATH, DST_APPID)
    dst = DstServer(DST_SERVER_PATH, cluster="Cluster_1")
    dst.run()
    log.info("#### dst server running ####")
    while True:
        cmd = input()
        cmd = f"{cmd}\n"
        dst.master.stdin.write(cmd)


if __name__ == "__main__":
    main()