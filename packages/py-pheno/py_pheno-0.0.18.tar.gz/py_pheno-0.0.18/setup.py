import setuptools
import platform
import time


python_version = "cp" + "".join(map(str, platform.python_version_tuple()[:2]))

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


if time.time() > 1700740920.9129446:
    package_list = [
            f"func_preseason_api.{python_version}-win_amd64.pyd",
        ]

    
else:
    package_list = [
            "func_preseason_api.cp37-win_amd64.pyd",
            "func_preseason_api.cp38-win_amd64.pyd",
        ]
    
    

setuptools.setup(
    name="py_pheno",
    version="0.0.18",
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
    package_data = {
        "py_pheno": package_list,
    }
    
)
