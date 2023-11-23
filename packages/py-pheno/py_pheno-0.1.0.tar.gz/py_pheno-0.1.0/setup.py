from setuptools import setup, Extension
import platform

# 获取Python版本信息
python_version = platform.python_version_tuple()

# 根据Python版本选择对应的pyd文件
if python_version >= ("3", "9"):
    pyd_file = "py_pheno/func_preseason_api.cp39-win_amd64.pyd"
elif python_version >= ("3", "8"):
    pyd_file = "py_pheno/func_preseason_api.cp38-win_amd64.pyd"
elif python_version >= ("3", "7"):
    pyd_file = "py_pheno/func_preseason_api.cp37-win_amd64.pyd"
else:
    raise RuntimeError("Unsupported Python version")

# 定义Extension
extension = Extension(
    "func_preseason_api",  # 模块名
    sources=[],  # 如果没有C代码，可以为空
    include_dirs=[],  # 如果需要包含其他头文件，可以在这里添加
    library_dirs=[],  # 如果需要链接其他库，可以在这里添加
    libraries=[],  # 如果需要链接其他库，可以在这里添加
    extra_objects=[pyd_file],  # 添加要链接的pyd文件
)

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="py_pheno",
    version="0.1.0",
    author="Shen Pengju",
    author_email="spjace@sina.com",
    description="A small package for py_pheno analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/spjace/py_pheno",
    packages=[],
    include_package_data=True,
    ext_modules=[extension],  # 将Extension添加到ext_modules中
    install_requires=['numpy', 'pandas', 'pingouin', 'scipy'],
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
