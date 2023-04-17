from setuptools import setup

setup(
    name='util',
    version='0.1.0',
    py_modules=['main'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'util = main:util',
        ],
    },
)