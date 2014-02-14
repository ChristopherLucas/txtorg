try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='TxtOrg',
    version='0.1.0',
    author='Dustin Tingley',
    author_email='dtingley@gov.harvard.edu',
    packages=['textorganizer'],
    scripts=['bin/txtorg'],
#    package_data={'textorganizer': ['training_text.txt']},
    license='LICENSE.txt',
    description='Tool to make organizing data for textual analysis easy and scalable',
    long_description=open('README.txt').read(),
    install_requires=['chardet'],
)
