# Copyright (C) 2022 twyleg
import os
from setuptools import find_packages, setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='seame_piracer',
    version=read('VERSION.txt'),
    author='Junho Kim',
    author_email='jhk00@kookmin.ac.kr',
    description='PiRacer Abstract Layer for SEA:ME DES proejct',
    license='GPL 3.0',
    keywords='piracer embedded abstraction',
    url='https://github.com/junho2000/custom_piracer_py',
    packages=find_packages(),
    include_package_data=True,
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    install_requires=[
        'wheel',
        'RPi.GPIO',
        'adafruit-circuitpython-pca9685',
        'adafruit-circuitpython-ina219',
        'adafruit-circuitpython-ssd1306',
        'opencv-python'
    ],
    entry_points={}
)
