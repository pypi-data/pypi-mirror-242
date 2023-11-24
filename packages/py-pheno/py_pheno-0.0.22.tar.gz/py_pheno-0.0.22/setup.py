import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py_pheno",
    version="0.0.22",
    author="Shen Pengju",
    author_email="spjace@sina.com",
    description="A small package for py_pheno analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/spjace/py_pheno",
    packages=setuptools.find_packages(),
    install_requires=['numpy', 'pandas', 'pingouin', 'scipy'],
    include_package_data=True,
    package_data={"py_pheno": ["func_preseason_api.cp37-win_amd64.pyd"]},
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='==3.7.*',
)
