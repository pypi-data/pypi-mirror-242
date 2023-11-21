from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='electricityapi',
    version='0.2.dev1',
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
    long_description_content_type='text/markdown',

    install_requires=['requests'],
)
