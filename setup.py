try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='TxtOrg',
    version='0.2.0',
    author='Christopher Lucas, Alex Storer, Dustin Tingley',
    author_email='lucas.christopherd@gmail.com',
    packages=['textorganizer'],
    scripts=['bin/txtorg'],
#    package_data={'textorganizer': ['training_text.txt']},
    license='LICENSE.txt',
    description='Tool to make organizing data for textual analysis easy and scalable',
    long_description=open('README.txt').read(),
    install_requires=['chardet','whoosh','snownlp'],
)
