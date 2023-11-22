# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 14:33:09 2023

@author: Calig
"""

from setuptools import setup, find_packages

setup(
    name='suwonii',
    version='0.1.0',
    author='J.SONG',
    author_email='junhyuck@theimc.co.kr',
    description='Suwon Buses Airquality measurement package developed based on Dask',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)