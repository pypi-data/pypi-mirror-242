import setuptools
import platform
import time
import os


python_version = "cp" + "".join(map(str, platform.python_version_tuple()[:2]))

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

    
    

setuptools.setup(
    name="py_pheno",
    version="0.0.19",
    author="Shen Pengju",
    author_email="spjace@sina.com",
    description="A small package for py_pheno analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/spjace/py_pheno",
    packages=setuptools.find_packages(),
    install_requires=['numpy', 'pandas', 'pingouin', 'scipy'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    
    include_package_data=True,

    
)


# 删除与 Python 版本不对应的 .pyd 文件
for root, dirs, files in os.walk("py_pheno"):
    for file in files:
        if file.endswith(".pyd"):
            if python_version not in file:
                os.remove(os.path.join(root, file))