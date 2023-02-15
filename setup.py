"""Setup config for the module."""

import setuptools

from distutils.core import setup

setup(
    setup_requires=['wheel'],
    url='https://ortelius.io',
    project_urls={
        'Project Repo': 'https://github.com/ortelius/ortelius_common',
        'Issues': 'https://github.com/ortelius/ortelius/issues',
        'Python Python API Documentation': 'https://github.com/ortelius/ortelius_common/blob/main/README.md'
        },
    author='Steve Taylor',
    author_email='steve@deployhub.com',
    name='ortelius_common',
    version='10.0.1',
    py_modules=['ortelius_common'],
    license='Apache-2.0',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    python_requires='>=3.6',
    include_package_data=True
)
