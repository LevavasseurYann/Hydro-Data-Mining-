from setuptools import setup, find_packages
import re
import os
cmd = 'pip3 install --upgrade pip'
os.system(cmd)

# ------------------

setup(
name = "workspace_internship",
version = "1.0",
description='M2 internship project',
packages=find_packages(),
author = "LEVAVASSEUR Yann",
author_email = "levavasseuryann@gmail.com",
)
