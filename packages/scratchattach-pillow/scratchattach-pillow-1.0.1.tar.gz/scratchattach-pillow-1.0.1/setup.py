from setuptools import setup, find_packages
import codecs
import os

VERSION = '1.0.1'
DESCRIPTION = 'An modded version of scratchattach'
LONG_DESCRIPTION = DESCRIPTION

# Setting up
setup(
    name="scratchattach-pillow",
    version=VERSION,
    author="mas6y6",
    author_email="",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=open('README.md').read(),
    packages=find_packages(),
    install_requires=["websocket-client","numpy","requests","bs4"],
    keywords=['scratch api', 'scratchattach', 'scratch api python', 'scratch python', 'scratch for python', 'scratch', 'scratch cloud', 'scratch cloud variables', 'scratch bot'],
    url='https://github.com/mas6y6/scratchattach-pillow',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
