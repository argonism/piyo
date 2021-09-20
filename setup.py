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

    description='esa API v1 client library, written in python', # パッケージの簡単な説明
    long_description=readme(), # PyPIに'Project description'として表示されるパッケージの説明文
    long_description_content_type='text/markdown' # long_descriptionの形式を'text/plain', 'text/x-rst', 'text/markdown'のいずれかから指定
    keywords='gokulang goku-lang', # PyPIでの検索用キーワードをスペース区切りで指定

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ], # パッケージ(プロジェクト)の分類。https://pypi.org/classifiers/に掲載されているものを指定可能。
)