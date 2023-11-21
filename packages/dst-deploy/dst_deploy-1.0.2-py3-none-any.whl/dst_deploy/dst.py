"""dst"""
import os
import shlex
import signal
import subprocess
import logging


log = logging.getLogger(__name__)


class DstServer:
    """饥荒服务"""

    def __init__(
        self,
        dst_server_path: str,
        cluster: str,
        only_master: bool = False,
    ) -> None:
        """饥荒服务管理.

        Args:
            dst_server_path (str): 饥荒服务启动命令路径.
            cluster (str): 存档名称.
            only_master (bool): 是否仅开启地面.
        """
        self.dst_server_path = dst_server_path
        self.initiator_path = os.path.join(self.dst_server_path, "bin64")
        self.cluster = cluster
        self.only_master = only_master
        # 服务进程
        self.master:  subprocess.Popen | None = None
        self.caves:  subprocess.Popen | None = None

    def _command_master(self) -> str:
        """构建master启动命令"""
        return f"./dontstarve_dedicated_server_nullrenderer_x64 -console -cluster {self.cluster} -shard Master"
    
    def _command_caves(self) -> str:
        """构建caves启动命令"""
        return f"./dontstarve_dedicated_server_nullrenderer_x64 -console -cluster {self.cluster} -shard Caves"

    def run(self) -> None:
        """运行饥荒服务"""
        self.master = self._popen(self._command_master())
        if not self.only_master:
            self.caves = self._popen(self._command_caves())

    def _popen(
        self,
        command: str,
    ) -> subprocess.Popen:
        """执行命令.

        Args:
            command (str): 命令

        Returns:
            subprocess.Popen: 进程.
        """
        log.info(f"command: {command}")
        process = subprocess.Popen(
            shlex.split(command),
            cwd=self.initiator_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            encoding="utf-8",
            bufsize=1,
        )
        return process

    def stop(self):
        """停止饥荒服务"""
        if self.master:
            self.master.send_signal(signal.SIGINT)
            self.master.wait()
        if self.caves:
            self.caves.send_signal(signal.SIGINT)
            self.caves.wait()

    def __del__(self):
        """资源回收"""
        self.stop()

