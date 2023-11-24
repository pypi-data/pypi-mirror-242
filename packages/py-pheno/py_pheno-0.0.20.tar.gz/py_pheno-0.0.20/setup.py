import setuptools
import platform
import time
import os


python_version = "cp" + "".join(map(str, platform.python_version_tuple()[:2]))

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

    
    

setuptools.setup(
    name="py_pheno",
    version="0.0.20",
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
package_dir = os.path.join(os.getcwd(), 'py_pheno')

for root, dirs, files in os.walk(package_dir):
    for file in files:
        if file.endswith(".pyd"):
            if python_version not in file:
                os.remove(os.path.join(root, file))
                print(os.path.join(root, file))