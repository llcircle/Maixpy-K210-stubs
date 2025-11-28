# setup.py
import os
from setuptools import setup

src_dir = "src"
py_modules = []
if os.path.isdir(src_dir):
    for f in os.listdir(src_dir):
        if f.endswith(".pyi"):
            py_modules.append(f[:-4])  # 去掉 .pyi

print("Stub modules:", sorted(py_modules))

setup(
    py_modules=sorted(set(py_modules)),
    package_dir={"": "src"},  # 顶级模块在 src/
)