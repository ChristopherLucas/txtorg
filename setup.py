try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='TxtOrg',
    version='1.0.0',
    author='Christopher Lucas, Alex Storer, Dustin Tingley',
    author_email='lucas.christopherd@gmail.com',
    packages=['textorganizer'],
    scripts=['bin/txtorg'],
    license='LICENSE.txt',
    description='Tool to make organizing data for textual analysis easy and scalable',
    install_requires=['chardet', 'snownlp'],
)
