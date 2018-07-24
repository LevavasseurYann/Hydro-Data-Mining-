#from setuptools import setup, find_packages
import re

# ------------------

setup(
name = "workspace_internship",
description = ("Internship M2"),
version = "1.0",
packages=['utils',],
license = "Mozilla Public License Version 2.0",
author = "LEVAVASSEUR Yann",
author_email = "levavasseuryann@gmail.com",
maintainer = "LEVAVASSEUR Yann",
maintainer_email = "levavasseuryann@gmail.com",
keywords = "python",
url = "https://github.com/LevavasseurYann/workspace_internship",
download_url = 'https://github.com/LevavasseurYann/workspace_internship.git',
test_suite='nose.collector',
tests_require=['nose'],
classifiers = [
	'Intended Audience :: Science/Research',
	'Intended Audience :: Developers',
	'Programming Language :: Python',
	'Topic :: Software Development',
	'Topic :: Scientific/Engineering',
	'Operating System :: Microsoft :: Windows',
	'Operating System :: Unix',
	'Operating System :: MacOS',
	'Programming Language :: Python :: 3.5',
	'Programming Language :: Python :: 3.6']
)
