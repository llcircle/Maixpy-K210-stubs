from typing import Tuple, List, Optional, Callable
"""Kendryte Neural Network Processor Unit | 神经网络处理器单元

Provides AI acceleration for K210 chip | 为K210芯片提供AI加速
"""

def load(model_path: str) -> int:
    """Load KPU model from file | 从文件加载KPU模型
    
    Args:
        model_path: Path to model file | 模型文件路径
    
    Returns:
        KPU model handle | KPU模型句柄
    
    Raises:
        OSError: If model file cannot be loaded | 如果无法加载模型文件，抛出OSError
    """
    ...


def run(kpu_net: int, input_data: bytes, task_id: int = 0) -> List[float]:
    """Run neural network inference | 运行神经网络推理
    
    Args:
        kpu_net: KPU model handle from load() | 从load()获得的KPU模型句柄
        input_data: Input data for inference | 用于推理的输入数据
        task_id: Task ID for asynchronous execution | 异步执行的任务ID
    
    Returns:
        Inference results as list of floats | 推理结果(浮点数列表)
    """
    ...


def deinit(kpu_net: int) -> None:
    """Deinitialize KPU network | 反初始化KPU网络
    
    Args:
        kpu_net: KPU model handle to release | 要释放的KPU模型句柄
    """
    ...
