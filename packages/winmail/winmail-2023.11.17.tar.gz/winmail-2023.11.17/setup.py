# -*- coding:utf-8 -*-

from setuptools import setup, find_packages


# from distutils.core import setup

INSTALL_REQUIRES = [
    'requests',
    'PyMySQL',
    'psycopg2',
    'pydantic',
    "pywin32; sys_platform == 'win32'"
]

setup(
    name='winmail',
    version='2023.11.17',
    python_requires='>=3.6.0',
    description='Winmail API',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Sway',
    author_email='sway_wang@foxmail.com',
    url='http://winmail.cn',
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES
)
