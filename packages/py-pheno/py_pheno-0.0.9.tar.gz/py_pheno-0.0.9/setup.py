import setuptools
import platform

# 获取Python版本信息
python_version = platform.python_version_tuple()

# 根据Python版本选择对应的pyd文件
if python_version >= ("3", "9"):
    pyd_file = "func_preseason_api.cp39-win_amd64.pyd"
elif python_version >= ("3", "8"):
    pyd_file = "func_preseason_api.cp38-win_amd64.pyd"
elif python_version >= ("3", "7"):
    pyd_file = "func_preseason_api.cp37-win_amd64.pyd"
else:
    raise RuntimeError("Unsupported Python version")

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py_pheno",
    version="0.0.9",
    author="Shen Pengju",
    author_email="spjace@sina.com",
    description="A small package for py_pheno analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/spjace/py_pheno",
    packages=setuptools.find_packages(),
    
    # 将选择的pyd文件添加到package_data
    package_data={'': [pyd_file]},
    
    install_requires=['numpy', 'pandas', 'pingouin', 'scipy'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
