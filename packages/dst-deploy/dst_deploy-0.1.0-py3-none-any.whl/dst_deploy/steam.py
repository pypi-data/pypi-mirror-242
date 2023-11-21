"""steam"""
import os
import logging

from pysteamcmdwrapper import SteamCMD, SteamCMDException, SteamCMD_command


log = logging.getLogger(__name__)


def init_dst_server(
    steam_path: str,
    dst_server_path: str,
    dst_appid: str,
):
    """安装DST_SERVER"""
    if not os.path.exists(steam_path):
        os.makedirs(steam_path)
    steam = SteamCMD(steam_path)
    # 安装steamcmd
    try:
        steam.install()
    except SteamCMDException:
        log.warning("Already installed, try to use the --force option to force installation")
    # 匿名登录
    login_anonymous = SteamCMD_command()
    login_anonymous.custom("+login anonymous ")
    steam.execute(login_anonymous)
    # 安装DST_SERVER
    steam.app_update(dst_appid, dst_server_path, validate=True)
