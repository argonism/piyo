from setuptools import setup
from codecs import open
from os import path


def readme():
    with open('README.md', encoding='utf-8') as f:
        return f.read()

setup(
    name='piyo',
    packages=['piyo'],

    version='0.2.0',

    license='MIT',

    install_requires=['requests'],

    author='k-ush',
    author_email='argoooooon@gmail.com',

    url='https://github.com/argonism/piyo',

    description='esa API v1 client library, written in python',
    long_description=readme(),
    long_description_content_type='text/markdown',
    keywords='esa api client esa.io python',

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)