from setuptools import setup, find_packages
import codecs
import os
VERSION = '0.0.4'
DESCRIPTION = 'lab help'
LONG_DESCRIPTION = 'lab help'
setup(
    name="revacnlab",
    version=VERSION,
    author="vmsubhash",
    author_email="subashmohan98@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'video', 'stream', 'video stream', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
