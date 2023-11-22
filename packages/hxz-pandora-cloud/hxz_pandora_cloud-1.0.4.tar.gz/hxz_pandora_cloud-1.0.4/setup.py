# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

from src.hxz_pandora_cloud import __version__

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='hxz_pandora_cloud',
    version=__version__,
    python_requires='>=3.7',
    author='Xiaozhou Huang',
    author_email='shoot82003@qq.com',
    keywords='OpenAI ChatGPT ChatGPT-Plus',
    description='A package for hxz_pandora-ChatGPT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/shoot82003/hxz_pandora_cloud',
    packages=find_packages('src'),
    package_dir={'hxz_pandora_cloud': 'src/hxz_pandora_cloud'},
    include_package_data=True,
    project_urls={
        'Source': 'https://github.com/shoot82003/hxz_pandora_cloud',
        'Tracker': 'https://github.com/shoot82003/hxz_pandora_cloud/issues',
    },
    classifiers=[
        'Development Status :: 4 - Beta',

        'Environment :: Web Environment',

        'Framework :: Flask',

        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',

        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',

        'Natural Language :: English',
        'Natural Language :: Chinese (Simplified)',

        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',

        'Programming Language :: JavaScript',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',

        'Topic :: Communications :: Chat',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
