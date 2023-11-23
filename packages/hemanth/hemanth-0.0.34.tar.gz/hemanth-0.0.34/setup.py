from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.34'
DESCRIPTION = 'hemanth'
LONG_DESCRIPTION = 'A package to integrate with phenom apis'

# Setting up
setup(
    name="hemanth",
    version=VERSION,
    author="hemanth",
    author_email="8297991468h@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['arithmetic', 'math', 'mathematics', 'python tutorial', 'avi upadhyay'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)