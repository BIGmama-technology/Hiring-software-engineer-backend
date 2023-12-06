from setuptools import setup, find_packages

setup(
    name='clientserverpkg',
    version='0.9',
    packages=find_packages(),
    install_requires=[
        'asyncio'
    ],
)
