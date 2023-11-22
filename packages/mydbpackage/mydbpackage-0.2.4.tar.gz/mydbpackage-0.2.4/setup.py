# setup.py
from setuptools import setup, find_packages

setup(
    name='mydbpackage',
    version='0.2.4',
    packages=find_packages(),
    install_requires=['mysql-connector-python'],
    entry_points={
        'console_scripts': [
            'your-command-name=mydbpackage.module_name:main',
        ],
    },
    description='A short description of my package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    test_suite='tests',
)
