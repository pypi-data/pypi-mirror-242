from setuptools import setup, find_packages

setup(
    name='netsys-client',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pywin32==306'
    ],
)
