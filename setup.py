# setup.py
import os
from setuptools import setup

# 动态扫描 src/ 下所有 .pyi 文件，提取模块名
src_dir = os.path.join(os.path.dirname(__file__), "src")
pyi_modules = []
if os.path.exists(src_dir):
    for filename in os.listdir(src_dir):
        if filename.endswith(".pyi"):
            module_name = filename[:-4]  # 去掉 .pyi
            pyi_modules.append(module_name)

# 注意：即使有 pyproject.toml，setuptools 也会读取 setup.py 中的 py_modules
setup(
    py_modules=pyi_modules,
)