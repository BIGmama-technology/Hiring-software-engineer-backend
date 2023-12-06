from setuptools import setup, find_packages

setup(
    name='p2ppkg',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'asyncio'
    ],
)
