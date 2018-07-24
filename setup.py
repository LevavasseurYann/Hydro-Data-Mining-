from setuptools import setup, find_packages
import re
import os
cmd1 = "pip3 install --upgrade pip3"
cmd2 = "pip3 install --upgrade setuptools"
os.system(cmd1)
os.system(cmd2)

# ------------------

setup(
name = "workspace_internship",
version = "1.0",
description='M2 internship project',
packages=find_packages(),
author = "LEVAVASSEUR Yann",
author_email = "levavasseuryann@gmail.com",
)
