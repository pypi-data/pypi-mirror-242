"""项目配置"""
import os
import logging

from .utils.env import Env


# 日志
logging.basicConfig(
    format='%(message)s',
    level=logging.INFO,
)

# HOME目录
HOME_PATH = os.path.expanduser("~")
# 是否debug模式
DEBUG = Env.boolean("DEBUG", False)
# steam安装路径
STEAM_PATH = Env.string("STEAM_PATH", default=os.path.join(HOME_PATH, "steamcmd"))
# dst安装位置
DST_SERVER_PATH = Env.string("DST_SERVER_PATH", default=os.path.join(HOME_PATH, "dst_server"))
# dst appid
DST_APPID = Env.int("DST_APPID", default=343050)