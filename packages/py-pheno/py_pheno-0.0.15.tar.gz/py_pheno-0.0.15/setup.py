import setuptools
import platform

python_version = "cp" + "".join(map(str, platform.python_version_tuple()[:2]))

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py_pheno",
    version="0.0.15",
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
    package_data = {
        "py_pheno": [
            f"func_preseason_api.{python_version}-win_amd64.pyd",
        ],
    },
    # include_package_data=True,
)
