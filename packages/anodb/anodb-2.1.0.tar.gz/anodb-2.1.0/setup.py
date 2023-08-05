from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="anodb",
    version="2.1.0",
    packages=find_packages(),
    author="Fabien Coelho",
    author_email="ano.db@coelho.net",
    url="https://github.com/zx80/anodb",
    install_requires=["aiosql>=3.2.0"],
    description="Convenient Wrapper around AioSQL and a Database Connection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        "Programming Language :: Python",
        "Programming Language :: SQL",
        "Topic :: Database :: Front-Ends",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
