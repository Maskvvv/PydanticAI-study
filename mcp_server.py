from fastmcp import FastMCP
import platform
import socket
import os
from datetime import datetime
from typing import Annotated

mcp = FastMCP("HostInfoServer")
'''
{
  "mcpServers": {
    "host-info-server": {
      "command": "uv",
      "args": [
        "--directory",
        "d:\\code\\ai\\PydanticAI-study",
        "run",
        "python",
        "mcp_server.py"
      ]
    }
  }
}

'''

@mcp.tool()
def get_system_info() -> str:
    """获取当前主机的系统信息，包括操作系统、架构、主机名等"""
    info = {
        "操作系统": platform.system(),
        "操作系统版本": platform.version(),
        "操作系统发行版": platform.release(),
        "架构": platform.machine(),
        "处理器": platform.processor(),
        "主机名": socket.gethostname(),
        "Python版本": platform.python_version(),
    }
    return "\n".join([f"{k}: {v}" for k, v in info.items()])


@mcp.tool()
def get_network_info() -> str:
    """获取当前主机的网络信息，包括IP地址等"""
    hostname = socket.gethostname()
    try:
        local_ip = socket.gethostbyname(hostname)
    except socket.gaierror:
        local_ip = "无法获取"
    
    info = {
        "主机名": hostname,
        "本地IP": local_ip,
        "FQDN": socket.getfqdn(),
    }
    return "\n".join([f"{k}: {v}" for k, v in info.items()])


@mcp.tool()
def get_environment_info() -> str:
    """获取当前主机的环境变量信息（仅显示常用环境变量）"""
    env_keys = [
        "USERNAME", "USER", "HOME", "USERPROFILE",
        "PATH", "PYTHONPATH", "TEMP", "TMP",
        "COMPUTERNAME", "OS", "PROCESSOR_ARCHITECTURE"
    ]
    info = {}
    for key in env_keys:
        value = os.environ.get(key, "未设置")
        if key == "PATH":
            value = value[:100] + "..." if len(value) > 100 else value
        info[key] = value
    
    return "\n".join([f"{k}: {v}" for k, v in info.items()])


@mcp.tool()
def get_time_info() -> str:
    """获取当前主机的日期和时间信息"""
    now = datetime.now()
    info = {
        "当前日期": now.strftime("%Y-%m-%d"),
        "当前时间": now.strftime("%H:%M:%S"),
        "星期": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][now.weekday()],
        "时区": str(now.astimezone().tzinfo),
    }
    return "\n".join([f"{k}: {v}" for k, v in info.items()])


@mcp.tool()
def get_disk_info() -> str:
    """获取当前主机的磁盘使用信息"""
    import shutil
    
    result = []
    if platform.system() == "Windows":
        drives = ["C:", "D:", "E:"]
    else:
        drives = ["/"]
    
    for drive in drives:
        try:
            usage = shutil.disk_usage(drive)
            total_gb = usage.total / (1024 ** 3)
            used_gb = usage.used / (1024 ** 3)
            free_gb = usage.free / (1024 ** 3)
            percent = (usage.used / usage.total) * 100
            result.append(
                f"{drive} - 总计: {total_gb:.1f}GB, "
                f"已用: {used_gb:.1f}GB ({percent:.1f}%), "
                f"可用: {free_gb:.1f}GB"
            )
        except Exception as e:
            result.append(f"{drive}: 无法获取信息 - {e}")
    
    return "\n".join(result)


if __name__ == "__main__":
    mcp.run(transport="stdio")
