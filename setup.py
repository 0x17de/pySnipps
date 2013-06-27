#!/usr/bin/python2

from distutils.core import setup

setup(name='pySnipps',
      version='0.3',
      description='A snippet tool written in python',
      author='Manuel Herrmann',
      author_email='pysnipps@icetruck.de',
      url='http://pysnipps.icetruck.de/',
	  scripts = ["pySnipps"],
      packages=["pySnipps"],
	  package_dir={'pySnipps': 'src/pySnipps'},
	  package_data={'pySnipps': ['resources/*']},
     )
