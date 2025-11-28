import os
from setuptools import setup

# 扫描 src/ 下所有 .pyi 文件，作为顶级模块
src_dir = "src"
if not os.path.isdir(src_dir):
    raise FileNotFoundError(f"Source directory '{src_dir}' not found")

py_modules = []
for filename in os.listdir(src_dir):
    if filename.endswith(".pyi"):
        mod_name = filename[:-4]  # 去掉 .pyi
        if mod_name.isidentifier():  # 确保是合法模块名
            py_modules.append(mod_name)

if not py_modules:
    raise RuntimeError("No .pyi files found in src/")

print("Found stub modules:", sorted(py_modules))

setup(
    name="MaixpyK210_stubs",
    version="0.1.0",
    description="Type stubs for MaixPy K210",
    package_dir={"": "src"},          # 顶级包内容在 src/
    py_modules=py_modules,            # 声明顶级模块
    packages=[],                      # 不使用包模式
    package_data={"": ["*.pyi", "py.typed"]},
    include_package_data=True,
    python_requires=">=3.9",
    zip_safe=False,
    # PEP 561: 声明这是一个类型 stub 包
    data_files=[("", ["src/py.typed"])],
)