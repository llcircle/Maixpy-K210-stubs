import os
from setuptools import setup

src_dir = "src"
if not os.path.isdir(src_dir):
    raise RuntimeError("src/ not found")

# 扫描 .pyi 文件
py_modules = []
for f in os.listdir(src_dir):
    if f.endswith(".pyi"):
        py_modules.append(f[:-4])

if not py_modules:
    raise RuntimeError("No .pyi files found")

print(">>> Installing stub modules:", py_modules)

setup(
    name="MaixpyK210_stubs",
    version="0.1.0",
    description="Type stubs for MaixPy K210",
    py_modules=py_modules,
    package_dir={"": "src"},
    packages=[],  # 不使用包模式
    include_package_data=True,
    package_data={"": ["*.pyi", "py.typed"]},
    python_requires=">=3.9",
)