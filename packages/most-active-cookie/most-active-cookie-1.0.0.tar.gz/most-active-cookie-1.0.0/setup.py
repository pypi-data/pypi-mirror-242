import os

from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

long_description = read('README.md') if os.path.isfile("README.md") else ""

setup(
    name='most-active-cookie',
    version="1.0.0",
    author='Chan Hong',
    author_email='hello@chanhong.xyz',
    description='Tools for extracting most active cookie from csv',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/yongchand/MostActiveCookie',
    packages=find_packages(exclude=['tests']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.8,<4',
    project_urls={
        'Bug Reports': 'https://github.com/yongchand/MostActiveCookie/issues',
        'Source': 'https://github.com/yongchand/MostActiveCookie',
    },
)