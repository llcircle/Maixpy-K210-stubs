from typing import List, Tuple, Optional

def listdir(path: str = '/') -> List[str]:
    """List directory contents | 列出目录内容
    
    Args:
        path: Directory path to list | 要列出的目录路径
    
    Returns:
        List of filenames in the directory | 目录中的文件名列表
    """
    ...

def mkdir(path: str) -> None:
    """Create directory | 创建目录
    
    Args:
        path: Directory path to create | 要创建的目录路径
    
    Raises:
        OSError: If directory already exists or cannot be created | 如果目录已存在或无法创建，抛出OSError
    """
    ...

def remove(path: str) -> None:
    """Remove file | 删除文件
    
    Args:
        path: File path to remove | 要删除的文件路径
    
    Raises:
        OSError: If file does not exist or cannot be removed | 如果文件不存在或无法删除，抛出OSError
    """
    ...

def rmdir(path: str) -> None:
    """Remove directory | 删除目录
    
    Args:
        path: Directory path to remove | 要删除的目录路径
    
    Raises:
        OSError: If directory does not exist, is not empty, or cannot be removed | 如果目录不存在、非空或无法删除，抛出OSError
    """
    ...

def stat(path: str) -> Tuple[int, int, int, int, int, int, int]:
    """Get file status | 获取文件状态
    
    Args:
        path: File path to get status for | 要获取状态的文件路径
    
    Returns:
        Tuple containing file information (st_mode, st_ino, st_dev, st_nlink, st_uid, st_gid, st_size) | 包含文件信息的元组(st_mode, st_ino, st_dev, st_nlink, st_uid, st_gid, st_size)
    """
    ...

def mount(fs, mount_point: str) -> None:
    """Mount filesystem | 挂载文件系统
    
    Args:
        fs: Filesystem object | 文件系统对象
        mount_point: Mount point path | 挂载点路径
    """
    ...

def umount(mount_point: str) -> None:
    """Unmount filesystem | 卸载文件系统
    
    Args:
        mount_point: Mount point path to unmount | 要卸载的挂载点路径
    """
    ...

def chdir(path: str) -> None:
    """Change current directory | 改变当前目录
    
    Args:
        path: New directory path | 新的目录路径
    """
    ...

def getcwd() -> str:
    """Get current working directory | 获取当前工作目录
    
    Returns:
        Current directory path | 当前目录路径
    """
    ...