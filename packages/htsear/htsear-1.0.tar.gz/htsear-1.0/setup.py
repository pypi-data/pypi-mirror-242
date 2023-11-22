import pathlib
from setuptools import setup, find_packages

setup(
    name='htsear',
    version='1.0',
    packages=find_packages(),
    description="htreader is a file treatment",
    long_description=pathlib.Path("README.md").read_text(),
    licenses=pathlib.Path("LICENSE").read_text(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Utilities",
    ],
    include_package_data=True,
    python_requires=">3.10, <3.11",
    author="RAKOTONIAINA Harry Yves",
    author_email="iharrysh.rakotoniaina@gmail.com",
    license=pathlib.Path("LICENSE").read_text()
)