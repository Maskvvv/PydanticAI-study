import os
import subprocess
from pathlib import Path
from pydantic_ai import RunContext


def create_text_file(ctx: RunContext, file_path: str, content: str) -> str:
    """创建文本文件
    
    Args:
        file_path: 文件路径
        content: 文件内容
    
    Returns:
        操作结果信息
    """
    try:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
        return f"成功创建文件: {file_path}"
    except Exception as e:
        return f"创建文件失败: {str(e)}"


def create_python_file(ctx: RunContext, file_path: str, content: str) -> str:
    """创建Python脚本文件
    
    Args:
        file_path: 文件路径
        content: Python代码内容
    
    Returns:
        操作结果信息
    """
    try:
        path = Path(file_path)
        if not file_path.endswith('.py'):
            file_path = file_path + '.py'
            path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
        return f"成功创建Python文件: {file_path}"
    except Exception as e:
        return f"创建Python文件失败: {str(e)}"


def get_directory_structure(ctx: RunContext, directory: str = ".") -> str:
    """获取目录结构
    
    Args:
        directory: 目录路径，默认为当前目录
    
    Returns:
        目录结构字符串
    """
    try:
        path = Path(directory)
        if not path.exists():
            return f"目录不存在: {directory}"
        
        result = []
        for item in sorted(path.rglob("*")):
            depth = len(item.relative_to(path).parts) - 1
            indent = "  " * depth
            if item.is_dir():
                result.append(f"{indent}📁 {item.name}/")
            else:
                size = item.stat().st_size
                result.append(f"{indent}📄 {item.name} ({size} bytes)")
        
        return "\n".join(result) if result else "空目录"
    except Exception as e:
        return f"获取目录结构失败: {str(e)}"


def rename_file(ctx: RunContext, old_path: str, new_path: str) -> str:
    """重命名或移动文件
    
    Args:
        old_path: 原文件路径
        new_path: 新文件路径
    
    Returns:
        操作结果信息
    """
    try:
        old = Path(old_path)
        new = Path(new_path)
        
        if not old.exists():
            return f"原文件不存在: {old_path}"
        
        new.parent.mkdir(parents=True, exist_ok=True)
        old.rename(new)
        return f"成功重命名: {old_path} -> {new_path}"
    except Exception as e:
        return f"重命名失败: {str(e)}"


def execute_windows_command(ctx: RunContext, command: str) -> str:
    """执行Windows命令
    
    Args:
        command: 要执行的命令
    
    Returns:
        命令执行结果
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        
        output = []
        if result.stdout:
            output.append(f"输出:\n{result.stdout}")
        if result.stderr:
            output.append(f"错误:\n{result.stderr}")
        output.append(f"返回码: {result.returncode}")
        
        return "\n".join(output)
    except Exception as e:
        return f"执行命令失败: {str(e)}"


def read_file(ctx: RunContext, file_path: str) -> str:
    """读取文件内容
    
    Args:
        file_path: 文件路径
    
    Returns:
        文件内容
    """
    try:
        path = Path(file_path)
        if not path.exists():
            return f"文件不存在: {file_path}"
        return path.read_text(encoding='utf-8')
    except Exception as e:
        return f"读取文件失败: {str(e)}"


def delete_file(ctx: RunContext, file_path: str) -> str:
    """删除文件
    
    Args:
        file_path: 文件路径
    
    Returns:
        操作结果信息
    """
    try:
        path = Path(file_path)
        if not path.exists():
            return f"文件不存在: {file_path}"
        path.unlink()
        return f"成功删除文件: {file_path}"
    except Exception as e:
        return f"删除文件失败: {str(e)}"
