from setuptools import setup, find_packages

setup(
    name="http_handle",
    version="0.0.1",
    packages=find_packages(),
    install_requires = [
        "requests==2.31.0"
    ],
    author="crzydev",
    description="http_handle"
)