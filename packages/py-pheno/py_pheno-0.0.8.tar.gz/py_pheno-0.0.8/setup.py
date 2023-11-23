import platform
from setuptools import setup, find_packages, Extension

# 获取当前Python版本信息
python_version = platform.python_version_tuple()

# 根据Python版本选择正确的pyd文件
if python_version[0] == '3' and python_version[1] == '9':
    pyd_file = 'func_preseason_api.cp39-win_amd64.pyd'
elif python_version[0] == '3' and python_version[1] == '8':
    pyd_file = 'func_preseason_api.cp38-win_amd64.pyd'
elif python_version[0] == '3' and python_version[1] == '7':
    pyd_file = 'func_preseason_api.cp37-win_amd64.pyd'
else:
    raise RuntimeError(f"Unsupported Python version: {platform.python_version()}")

# 设置Extension对象
ext_modules = [
    Extension('py_pheno', [pyd_file]),
]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="py_pheno",
    version="0.0.8",
    author="Shen Pengju",
    author_email="spjace@sina.com",
    description="A small package for py_pheno analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/spjace/py_pheno",
    packages=find_packages(),
    include_package_data=True,
    ext_modules=ext_modules,
    install_requires=['numpy', 'pandas', 'pingouin', 'scipy'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
