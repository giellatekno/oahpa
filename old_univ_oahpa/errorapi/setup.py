import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='errorapi',
    version='0.1',
    packages=['errorapi'],
    include_package_data=True,
    license='BSD License',
    description='A module for Oahpa to provide error feedback',
    long_description=README,
    url='http://giellatekno.uit.no/',
    author='Ryan Johnson',
    author_email='ryan.txanson@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License', # example license
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.8',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)

