from setuptools import setup, find_packages

long_description ='''
This packages gives you interfaces to various providers of electricity grid data.

Currently we only support electricitymap.org but are planing to add many more. Please leave a comment or pr if you want
to contribute more providers.
'''

setup(
    name='electricityapi',
    version='0.1.dev1',
    packages=find_packages(),
    url='https://github.com/green-coding-berlin/electricityapi',
    author='Didi Hoffmann',
    author_email='didi@green-coding.berlin',
    license='GNU AFFERO GENERAL PUBLIC LICENSE',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    description='This packages gives you interfaces to various providers of electricity grid data',
    long_description=long_description,

    install_requires=['requests'],
)
