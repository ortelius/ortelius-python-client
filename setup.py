"""Setup config for the module."""

from setuptools import find_packages, setup

setup(
    setup_requires=["wheel"],
    url="https://ortelius.io",
    project_urls={
        "Project Repo": "https://github.com/ortelius/ortelius",
        "Issues": "https://github.com/ortelius/ortelius/issues",
        "Python Python API Documentation": "https://github.com/ortelius/ortelius-python/blob/main/README.md",
    },
    author="Steve Taylor",
    author_email="steve@deployhub.com",
    name="ortelius",
    version="11.0.0",
    py_modules=["ortelius"],
    license="Apache-2.0",
    long_description=open("README.md", mode="r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    packages=find_packages(),
    include_package_data=True,
)
