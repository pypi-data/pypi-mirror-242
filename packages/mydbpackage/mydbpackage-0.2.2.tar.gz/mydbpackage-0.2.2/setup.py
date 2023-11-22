# setup.py
from setuptools import setup, find_packages

setup(
    name='mydbpackage',
    version='0.2.2',
    packages=find_packages(),
    install_requires=['mysql-connector-python'],
    entry_points={
        'console_scripts': [
            'your-command-name=mydbpackage.module_name:main',
        ],
    },
    test_suite='tests',
)
