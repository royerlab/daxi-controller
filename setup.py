"""
setup.py for daxi
"""
from os import path
import setuptools


setuptools.setup(
    name="daxi",
    version="0.0.0.dev0",
    author="",
    author_email="",
    license="",
    description="",
    long_description="",
    long_description_content_type="text/markdown",
    url="",
    project_urls={
        "Bug Tracker": "",
    },
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
    ],
    package_dir={"": f".{path.sep}"},
    packages=setuptools.find_packages(),
    install_requires="",
    python_requires=">=3.9",
)